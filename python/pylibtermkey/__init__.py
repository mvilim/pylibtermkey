import pylibtermkey_cpp
from pylibtermkey_cpp import TermKey as _TermKey, TermKeyKey as _TermKeyKey, TermKeyResult as _TermKeyResult, \
    TermKeyFlag as _TermKeyFlag, TermKeyCanon as _TermKeyCanon, TermKeyFormat as _TermKeyFormat, \
    TermKeySym as _TermKeySym, TermKeyType as _TermKeyType
from enum import IntEnum

from typing import Set, Tuple

__version__ = pylibtermkey_cpp.__version__


class TermKeyFlag(IntEnum):
    NOINTERPRET = _TermKeyFlag.NOINTERPRET
    CONVERTKP = _TermKeyFlag.CONVERTKP
    RAW = _TermKeyFlag.RAW
    UTF8 = _TermKeyFlag.UTF8
    NOTERMIOS = _TermKeyFlag.NOTERMIOS
    SPACESYMBOL = _TermKeyFlag.SPACESYMBOL
    CTRLC = _TermKeyFlag.CTRLC
    EINTR = _TermKeyFlag.EINTR
    NOSTART = _TermKeyFlag.NOSTART


class TermKeyCanon(IntEnum):
    SPACESYMBOL = _TermKeyCanon.SPACESYMBOL
    DELBS = _TermKeyCanon.DELBS


class TermKeyResult(IntEnum):
    NONE = _TermKeyResult.NONE
    KEY = _TermKeyResult.KEY
    EOF = _TermKeyResult.EOF
    AGAIN = _TermKeyResult.AGAIN
    ERROR = _TermKeyResult.ERROR


class TermKeyFormat(IntEnum):
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


class TermKeySym(IntEnum):
    UNKNOWN = _TermKeySym.UNKNOWN
    NONE = _TermKeySym.NONE
    BACKSPACE = _TermKeySym.BACKSPACE
    TAB = _TermKeySym.TAB
    ENTER = _TermKeySym.ENTER
    ESCAPE = _TermKeySym.ESCAPE
    SPACE = _TermKeySym.SPACE
    DEL = _TermKeySym.DEL
    UP = _TermKeySym.UP
    DOWN = _TermKeySym.DOWN
    LEFT = _TermKeySym.LEFT
    RIGHT = _TermKeySym.RIGHT
    BEGIN = _TermKeySym.BEGIN
    FIND = _TermKeySym.FIND
    INSERT = _TermKeySym.INSERT
    DELETE = _TermKeySym.DELETE
    SELECT = _TermKeySym.SELECT
    PAGEUP = _TermKeySym.PAGEUP
    PAGEDOWN = _TermKeySym.PAGEDOWN
    HOME = _TermKeySym.HOME
    END = _TermKeySym.END
    CANCEL = _TermKeySym.CANCEL
    CLEAR = _TermKeySym.CLEAR
    CLOSE = _TermKeySym.CLOSE
    COMMAND = _TermKeySym.COMMAND
    COPY = _TermKeySym.COPY
    EXIT = _TermKeySym.EXIT
    HELP = _TermKeySym.HELP
    MARK = _TermKeySym.MARK
    MESSAGE = _TermKeySym.MESSAGE
    MOVE = _TermKeySym.MOVE
    OPEN = _TermKeySym.OPEN
    OPTIONS = _TermKeySym.OPTIONS
    PRINT = _TermKeySym.PRINT
    REDO = _TermKeySym.REDO
    REFERENCE = _TermKeySym.REFERENCE
    REFRESH = _TermKeySym.REFRESH
    REPLACE = _TermKeySym.REPLACE
    RESTART = _TermKeySym.RESTART
    RESUME = _TermKeySym.RESUME
    SAVE = _TermKeySym.SAVE
    SUSPEND = _TermKeySym.SUSPEND
    UNDO = _TermKeySym.UNDO
    KP0 = _TermKeySym.KP0
    KP1 = _TermKeySym.KP1
    KP2 = _TermKeySym.KP2
    KP3 = _TermKeySym.KP3
    KP4 = _TermKeySym.KP4
    KP5 = _TermKeySym.KP5
    KP6 = _TermKeySym.KP6
    KP7 = _TermKeySym.KP7
    KP8 = _TermKeySym.KP8
    KP9 = _TermKeySym.KP9
    KPENTER = _TermKeySym.KPENTER
    KPPLUS = _TermKeySym.KPPLUS
    KPMINUS = _TermKeySym.KPMINUS
    KPMULT = _TermKeySym.KPMULT
    KPDIV = _TermKeySym.KPDIV
    KPCOMMA = _TermKeySym.KPCOMMA
    KPPERIOD = _TermKeySym.KPPERIOD
    KPEQUALS = _TermKeySym.KPEQUALS
    N_SYMS = _TermKeySym.N_SYMS


class TermKeyType(IntEnum):
    UNICODE = _TermKeyType.UNICODE
    FUNCTION = _TermKeyType.FUNCTION
    KEYSYM = _TermKeyType.KEYSYM
    MOUSE = _TermKeyType.MOUSE
    POSITION = _TermKeyType.POSITION
    MODEREPORT = _TermKeyType.MODEREPORT
    DCS = _TermKeyType.DCS
    OSC = _TermKeyType.OSC
    UNKNOWN_CSI = _TermKeyType.UNKNOWN_CSI


class TermKeyKey:
    def __init__(self, tkk: _TermKeyKey):
        self.tkk = tkk

    def type(self) -> TermKeyType:
        return TermKeyType(self.tkk.type());

    def code(self):
        code = self.tkk.code()
        if self.type() is TermKeyType.KEYSYM:
            code = TermKeySym(int(code))
        return code

    def modifiers(self) -> int:
        return self.tkk.modifiers();

    def utf8(self) -> int:
        return self.tkk.utf8();


def get_errno() -> int:
    return pylibtermkey_cpp.get_errno()


def set_errno(code: int):
    pylibtermkey_cpp.set_errno(code)


class TermKey:
    def __init__(self, flags: Set[TermKeyFlag] = None):
        if flags is None:
            flags = set()
        self.tk = _TermKey({_TermKeyFlag(flag) for flag in flags})

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
        return self.tk.strfkey(key.tkk, _TermKeyFormat(format))

    def start(self) -> int:
        return self.tk.start()

    def stop(self) -> int:
        return self.tk.stop()

    def is_started(self) -> bool:
        return self.tk.is_started()

    def get_flags(self) -> Set[TermKeyFlag]:
        return {TermKeyFlag(int(flag)) for flag in self.tk.get_flags()}

    def set_flags(self, newflags: Set[TermKeyFlag]) -> None:
        self.tk.set_flags({_TermKeyFlag(flag) for flag in newflags})

    def get_waittime(self) -> int:
        return self.tk.get_waittime()

    def set_waittime(self, msec: int) -> None:
        self.tk.set_waittime(msec)

    def get_canonflags(self) -> Set[TermKeyCanon]:
        return {TermKeyCanon(int(flag)) for flag in self.tk.get_canonflags()}

    def set_canonflags(self, newcanonflags: Set[TermKeyCanon]) -> None:
        self.tk.set_canonflags({_TermKeyCanon(flag) for flag in newcanonflags})

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
