import pylibtermkey_cpp
from pylibtermkey_cpp import TermKey as _TermKey, TermKeyKey as _TermKeyKey, TermKeyResult as _TermKeyResult, \
    TermKeyFlag as _TermKeyFlag, TermKeyCanon as _TermKeyCanon, TermKeyFormat as _TermKeyFormat
from enum import Enum

from typing import Set, Tuple

__version__ = pylibtermkey_cpp.__version__


class TermKeyFlag(_TermKeyFlag):
    NOINTERPRET = _TermKeyFlag.NOINTERPRET
    CONVERTKP = _TermKeyFlag.CONVERTKP
    RAW = _TermKeyFlag.RAW
    UTF8 = _TermKeyFlag.UTF8
    NOTERMIOS = _TermKeyFlag.NOTERMIOS
    SPACESYMBOL = _TermKeyFlag.SPACESYMBOL
    CTRLC = _TermKeyFlag.CTRLC
    EINTR = _TermKeyFlag.EINTR
    NOSTART = _TermKeyFlag.NOSTART


class TermKeyCanon(_TermKeyCanon):
    SPACESYMBOL = _TermKeyCanon.SPACESYMBOL
    DELBS = _TermKeyCanon.DELBS


class TermKeyResult(_TermKeyResult):
    NONE = _TermKeyResult.NONE
    KEY = _TermKeyResult.KEY
    EOF = _TermKeyResult.EOF
    AGAIN = _TermKeyResult.AGAIN
    ERROR = _TermKeyResult.ERROR


class TermKeyFormat(_TermKeyFormat):
    LONGMOD = _TermKeyFormat.LONGMOD
    CARETCTRL = _TermKeyFormat.CARETCTRL
    ALTISMETA = _TermKeyFormat.ALTISMETA
    WRAPBRACKET = _TermKeyFormat.WRAPBRACKET
    SPACEMOD = _TermKeyFormat.SPACEMOD
    LOWERMOD = _TermKeyFormat.LOWERMOD
    LOWERSPACE = _TermKeyFormat.LOWERSPACE
    MOUSE_POS = _TermKeyFormat.MOUSE_POS
    VIM = _TermKeyFormat.VIM
    URWID = _TermKeyFormat.URWID


class TermKeyKey:
    def __init__(self, tkk: _TermKeyKey):
        self.tkk = tkk


def get_errno() -> int:
    return pylibtermkey_cpp.get_errno()


def set_errno(code: int):
    pylibtermkey_cpp.set_errno(code)


class TermKey:
    def __init__(self, flags: Set[TermKeyFlag] = None):
        if flags is None:
            flags = set()
        self.tk = _TermKey(flags)

    def check_version(self, major: int, minor: int) -> bool:
        return self.tk.check_version(major, minor)

    def getkey(self) -> Tuple[TermKeyResult, TermKeyKey]:
        t = self.tk.getkey()
        return TermKeyResult(t[0]), TermKeyKey(t[1])

    def getkey_force(self) -> Tuple[TermKeyResult, TermKeyKey]:
        t = self.tk.getkey_force()
        return TermKeyResult(t[0]), TermKeyKey(t[1])

    def waitkey(self) -> Tuple[TermKeyResult, TermKeyKey]:
        t = self.tk.waitkey()
        return TermKeyResult(t[0]), TermKeyKey(t[1])

    def advisereadable(self) -> bool:
        return self.tk.advisereadable()

    def strfkey(self, key: TermKeyKey, format: TermKeyFormat) -> str:
        return self.tk.strfkey(key.tkk, format)

    def start(self) -> int:
        return self.tk.start()

    def stop(self) -> int:
        return self.tk.stop()

    def is_started(self) -> bool:
        return self.tk.is_started()

    def get_flags(self) -> Set[TermKeyFlag]:
        return self.tk.get_flags()

    def set_flags(self, newflags: Set[TermKeyFlag]) -> None:
        self.tk.set_flags(newflags)

    def get_waittime(self) -> int:
        return self.tk.get_waittime()

    def set_waittime(self, msec: int) -> None:
        self.tk.set_waittime(msec)

    def get_canonflags(self) -> Set[TermKeyCanon]:
        return self.tk.get_canonflags()

    def set_canonflags(self, newcanonflags: Set[TermKeyCanon]) -> None:
        self.tk.set_canonflags(newcanonflags)

    def get_buffer_size(self) -> int:
        return self.tk.get_buffersize()

    def set_buffer_size(self, size: int) -> int:
        return self.tk.set_buffersize(size)

    def get_buffer_remaining(self) -> int:
        return self.tk.get_buffer_remaining()

    def canonicalise(self, key: TermKeyKey) -> None:
        return self.tk.canonicalise(key.tkk)

    def keycmp(self, key1: TermKeyKey, key2: TermKeyKey) -> int:
        return self.tk.keycmp(key1.tkk, key2.tkk)

    def push_bytes(self, b: bytes) -> None:
        return self.tk.push_bytes(b)
