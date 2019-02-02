# Copyright (c) 2019 Michael Vilim
# 
# This file is part of the pylibtermkey library. It is currently hosted at
# https://github.com/mvilim/pylibtermkey
# 
# pylibtermkey is licensed under the MIT license. A copy of the license can be
# found in the root folder of the project.

import abc

import unittest
from unittest import TestCase
import warnings

try:
    import curses
    curses.setupterm()
    bs_str = '<Backspace>'
    if curses.tigetstr('kbs') == bytes.fromhex('7F'):
        del_str = bs_str
    else:
        del_str = '<DEL>'
    has_curses = True
except:
    has_curses = False

try:
    from pynput.keyboard import Key, Controller

    def suppress_deprecation(action):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            action()
    has_pynput = True
except:
    has_pynput = False

import pylibtermkey as termkey


class Keys:
    CTRL = 1
    DEL = 2
    ESC = 3


class TermKeyTests(abc.ABC):
    def setUp(self):
        self.tk = termkey.TermKey()

    def tearDown(self):
        self.tk.stop()


class NonInputTests(TermKeyTests, TestCase):
    def test_new_flags(self):
        new_flags = {termkey.TermKeyFlag.CTRLC}
        self.tk.set_flags(new_flags)
        self.assertSetEqual(self.tk.get_flags(), new_flags)

    def test_wait(self):
        default_time = 50 
        new_time = 25
        self.assertEqual(self.tk.get_waittime(), default_time)
        self.tk.set_waittime(new_time)
        self.assertEqual(self.tk.get_waittime(), new_time)

    def test_new_canonflags(self):
        new_canonflags = {termkey.TermKeyCanon.DELBS}
        self.tk.set_canonflags(new_canonflags)
        self.assertSetEqual(self.tk.get_canonflags(), new_canonflags)


class InputTests(TermKeyTests, abc.ABC):
    @abc.abstractmethod
    def tap(self, key):
        pass

    @abc.abstractmethod
    def modify_tap(self, key, modifier):
        pass

    def test_wait_simple_letter(self):
        letter = 'j'
        self.tap(letter)
        res, key = self.tk.waitkey()
        self.assertEqual(res, termkey.TermKeyResult.KEY)
        self.assertEqual(self.tk.strfkey(key, termkey.TermKeyFormat.VIM), letter)

    def test_get(self):
        letter = 'j'
        self.tap(letter)
        res, key = self.tk.getkey()
        self.assertEqual(res, termkey.TermKeyResult.KEY)
        self.assertEqual(self.tk.strfkey(key, termkey.TermKeyFormat.VIM), letter)

    def test_force_get(self):
        self.tap(Keys.ESC)
        res, key = self.tk.getkey()
        self.assertEqual(res, termkey.TermKeyResult.AGAIN)
        res, key = self.tk.getkey_force()
        self.assertEqual(res, termkey.TermKeyResult.KEY)
        self.assertEqual(self.tk.strfkey(key, termkey.TermKeyFormat.VIM), '<Escape>')

    def test_ctrlc_flag(self):
        self.tk.set_flags({termkey.TermKeyFlag.CTRLC})
        # restart termkey to pick up the new interrupt behavior
        self.tk.stop()
        self.tk.start()
        self.modify_tap('c', Keys.CTRL)
        res, key = self.tk.waitkey()
        self.assertEqual(res, termkey.TermKeyResult.KEY)
        self.assertEqual(self.tk.strfkey(key, termkey.TermKeyFormat.VIM), '<C-c>')

    @unittest.skipUnless(has_curses, "Requires curses to query terminfo DEL mapping")
    def test_canonicalize(self):
        self.tap(Keys.DEL)
        res, key = self.tk.waitkey()
        self.assertEqual(res, termkey.TermKeyResult.KEY)
        self.assertEqual(self.tk.strfkey(key, termkey.TermKeyFormat.VIM), del_str)
        self.tk.set_canonflags({termkey.TermKeyCanon.DELBS})
        self.tk.canonicalise(key)
        self.assertEqual(self.tk.strfkey(key, termkey.TermKeyFormat.VIM), bs_str)

    def test_key_symbol(self):
        self.tap(Keys.ESC)
        res, key = self.tk.getkey_force()
        self.assertEqual(res, termkey.TermKeyResult.KEY)
        self.assertEqual(key.code(), termkey.TermKeySym.ESCAPE)


@unittest.skipUnless(has_pynput, "Requires pynput (and thus a real input mechanism, like an X server)")
class RealInputTests(InputTests, TestCase):
    def setUp(self):
        super(InputTests, self).setUp()
        self.k = Controller()

    def tearDown(self):
        super(InputTests, self).tearDown()

    def map_key(self, key):
        kmap = self.keymap()
        if isinstance(key, str):
            return key
        elif key in kmap:
            return kmap[key]
        else:
            raise Exception('Could not find {} key in keymap'.format(key))

    def tap(self, key):
        def tap():
            mkey = self.map_key(key)
            self.k.press(mkey)
            self.k.release(mkey)

        suppress_deprecation(tap)
        self.tk.advisereadable()

    def modify_tap(self, key, modifier):
        def modify_tap():
            mkey = self.map_key(key)
            mmod = self.map_key(modifier)
            self.k.press(mmod)
            self.k.press(mkey)
            self.k.release(mkey)
            self.k.release(mmod)
        suppress_deprecation(modify_tap)

    def keymap(self):
        return {Keys.CTRL: Key.ctrl, Keys.DEL: Key.backspace, Keys.ESC: Key.esc}


class FakeInputTests(InputTests, TestCase):
    def map_key(self, key):
        kmap = self.keymap()
        if isinstance(key, str):
            return bytes(key, 'utf8')
        elif key in kmap:
            return kmap[key]
        else:
            raise Exception('Could not find {} key in keymap'.format(key))

    def tap(self, key):
        mkey = self.map_key(key)
        self.tk.push_bytes(mkey)

    def modify_tap(self, key, modifier):
        if (modifier is Keys.CTRL) and (key is 'c'):
            self.tk.push_bytes(bytes.fromhex('03'))
        else:
            raise Exception('Other modifiers supported in fake input testing')

    def keymap(self):
        return {Keys.DEL: bytes.fromhex('7F'), Keys.ESC: bytes.fromhex('1b')}


if __name__ == '__main__':
    unittest.main()
