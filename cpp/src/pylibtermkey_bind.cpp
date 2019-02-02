// Copyright (c) 2019 Michael Vilim
//
// This file is part of the pylibtermkey library. It is currently hosted at
// https://github.com/mvilim/pylibtermkey
//
// pylibtermkey is licensed under the MIT license. A copy of the license can be
// found in the root folder of the project.

#include <errno.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <termkey.h>
#include <memory>
#include <string>

namespace py = pybind11;

using std::string;
using std::unique_ptr;

// create a make_unique replacement to be C++11 compatible
template <typename T, typename... Args>
unique_ptr<T> make_unique(Args &&... args) {
    return unique_ptr<T>(new T(std::forward<Args>(args)...));
}

class TermKeyWrapper {
    TermKey *tk;

   public:
    TermKeyWrapper(int flags) { tk = termkey_new(0, flags); }

    TermKeyWrapper(const char *term, int flags) {
        tk = termkey_new_abstract(term, flags);
    }

    ~TermKeyWrapper() { destroy(); }

    void check_version(int major, int minor) {
        return termkey_check_version(major, minor);
    }

    void free() { termkey_free(tk); };
    void destroy() { termkey_destroy(tk); };

    int start() { return termkey_start(tk); }
    int stop() { return termkey_stop(tk); }
    int is_started() { return termkey_is_started(tk); }

    int get_fd() { return termkey_get_fd(tk); }

    int get_flags() { return termkey_get_flags(tk); }
    void set_flags(int newflags) { termkey_set_flags(tk, newflags); }

    int get_waittime() { return termkey_get_waittime(tk); }
    void set_waittime(int msec) { termkey_set_waittime(tk, msec); }

    int get_canonflags() { return termkey_get_canonflags(tk); }
    void set_canonflags(int newcanonflags) {
        termkey_set_canonflags(tk, newcanonflags);
    }

    size_t get_buffer_size() { return termkey_get_buffer_size(tk); }
    int set_buffer_size(size_t size) {
        return termkey_set_buffer_size(tk, size);
    }

    size_t get_buffer_remaining() { return termkey_get_buffer_remaining(tk); }

    void canonicalise(TermKeyKey *key) { termkey_canonicalise(tk, key); }

    TermKeyResult getkey(TermKeyKey *key) { return termkey_getkey(tk, key); }
    TermKeyResult getkey_force(TermKeyKey *key) {
        return termkey_getkey_force(tk, key);
    }
    TermKeyResult waitkey(TermKeyKey *key) { return termkey_waitkey(tk, key); }

    TermKeyResult advisereadable() { return termkey_advisereadable(tk); }

    size_t push_bytes(const char *bytes, size_t len) {
        return termkey_push_bytes(tk, bytes, len);
    }

    TermKeySym register_keyname(TermKeySym sym, const char *name) {
        return termkey_register_keyname(tk, sym, name);
    }
    const char *get_keyname(TermKeySym sym) {
        return termkey_get_keyname(tk, sym);
    }
    const char *lookup_keyname(const char *str, TermKeySym *sym) {
        return termkey_lookup_keyname(tk, str, sym);
    }

    TermKeySym keyname2sym(const char *keyname) {
        return termkey_keyname2sym(tk, keyname);
    }

    TermKeyResult interpret_mouse(const TermKeyKey *key,
                                  TermKeyMouseEvent *event, int *button,
                                  int *line, int *col) {
        return termkey_interpret_mouse(tk, key, event, button, line, col);
    }

    TermKeyResult interpret_position(const TermKeyKey *key, int *line,
                                     int *col) {
        return termkey_interpret_position(tk, key, line, col);
    }

    TermKeyResult interpret_modereport(const TermKeyKey *key, int *initial,
                                       int *mode, int *value) {
        return termkey_interpret_modereport(tk, key, initial, mode, value);
    }

    TermKeyResult interpret_csi(const TermKeyKey *key, long args[],
                                size_t *nargs, unsigned long *cmd) {
        return termkey_interpret_csi(tk, key, args, nargs, cmd);
    }

    TermKeyResult interpret_string(const TermKeyKey *key, const char **strp) {
        return termkey_interpret_string(tk, key, strp);
    }

    size_t strfkey(char *buffer, size_t len, TermKeyKey *key,
                   TermKeyFormat format) {
        return termkey_strfkey(tk, buffer, len, key, format);
    }
    const char *strpkey(const char *str, TermKeyKey *key,
                        TermKeyFormat format) {
        return termkey_strpkey(tk, str, key, format);
    }

    int keycmp(const TermKeyKey *key1, const TermKeyKey *key2) {
        return termkey_keycmp(tk, key1, key2);
    }
};

enum class TermKeyFlag {
    NOINTERPRET = TERMKEY_FLAG_NOINTERPRET,
    CONVERTKP = TERMKEY_FLAG_CONVERTKP,
    RAW = TERMKEY_FLAG_RAW,
    UTF8 = TERMKEY_FLAG_UTF8,
    NOTERMIOS = TERMKEY_FLAG_NOTERMIOS,
    SPACESYMBOL = TERMKEY_FLAG_SPACESYMBOL,
    CTRLC = TERMKEY_FLAG_CTRLC,
    _EINTR = TERMKEY_FLAG_EINTR,  // prefixed to avoid keyword conflict
    NOSTART = TERMKEY_FLAG_NOSTART
};

enum class TermKeyKeyMod {
    SHIFT = TERMKEY_KEYMOD_SHIFT,
    ALT = TERMKEY_KEYMOD_ALT,
    CTRL = TERMKEY_KEYMOD_CTRL
};

enum class TermKeyCanon {
    SPACESYMBOL = TERMKEY_CANON_SPACESYMBOL,
    DELBS = TERMKEY_CANON_DELBS
};

int combine_flags(py::set flags, string enum_name) {
    py::object enum_type =
        py::module::import("pylibtermkey_cpp").attr(enum_name.c_str());

    try {
        int combined_flags = 0;
        for (auto flag : flags) {
            if (py::isinstance(flag, enum_type)) {
                combined_flags = combined_flags | py::cast<int>(flag);
            } else {
                throw std::runtime_error("Invalid flag type received");
            }
        }
        return combined_flags;
    } catch (const std::runtime_error &re) {
        std::throw_with_nested(std::runtime_error("Could not convert flags: " +
                                                  string(re.what())));
    } catch (const std::exception &ex) {
        std::throw_with_nested(std::runtime_error("Could not convert flags: " +
                                                  string(ex.what())));
    }
}

py::set interpret_flags(int flags, string enum_name) {
    py::set flag_set;
    py::list all_flags = py::module::import("pylibtermkey_cpp")
                             .attr(enum_name.c_str())
                             .attr("__members__")
                             .attr("values")();
    for (auto flag : all_flags) {
        if ((py::cast<int>(flag) & flags) != 0) {
            flag_set.add(flag);
        }
    }
    return flag_set;
}

TermKeyResult getkey(TermKeyWrapper &tk, TermKeyKey *key) {
    py::gil_scoped_release release;
    return tk.getkey(key);
}

TermKeyResult getkey_force(TermKeyWrapper &tk, TermKeyKey *key) {
    py::gil_scoped_release release;
    return tk.getkey_force(key);
}

TermKeyResult waitkey(TermKeyWrapper &tk, TermKeyKey *key) {
    py::gil_scoped_release release;
    return tk.waitkey(key);
}

PYBIND11_MODULE(pylibtermkey_cpp, m) {
    py::class_<TermKeyWrapper>(m, "TermKey")
        .def(py::init([](py::set flags) {
                 return make_unique<TermKeyWrapper>(
                     combine_flags(flags, "TermKeyFlag"));
             }),
             py::arg("flags") = py::set())
        .def("check_version", &TermKeyWrapper::check_version)
        .def("getkey",
             [](TermKeyWrapper &tk) {
                 unique_ptr<TermKeyKey> key = make_unique<TermKeyKey>();
                 TermKeyResult result = getkey(tk, key.get());
                 return py::make_tuple(result, std::move(key));
             },
             py::return_value_policy::take_ownership)
        .def("getkey_force",
             [](TermKeyWrapper &tk) {
                 unique_ptr<TermKeyKey> key = make_unique<TermKeyKey>();
                 TermKeyResult result = getkey_force(tk, key.get());
                 return py::make_tuple(result, std::move(key));
             },
             py::return_value_policy::take_ownership)
        .def("waitkey",
             [](TermKeyWrapper &tk) {
                 unique_ptr<TermKeyKey> key = make_unique<TermKeyKey>();
                 TermKeyResult result = waitkey(tk, key.get());
                 return py::make_tuple(result, std::move(key));
             },
             py::return_value_policy::take_ownership)
        .def("advisereadable", &TermKeyWrapper::advisereadable)
        .def("strfkey",
             [](TermKeyWrapper &tk, TermKeyKey &key, TermKeyFormat format) {
                 char buffer[50];
                 tk.strfkey(buffer, sizeof buffer, &key, format);
                 return string(buffer);
             })
        .def("start", &TermKeyWrapper::start)
        .def("stop", &TermKeyWrapper::stop)
        .def("is_started", &TermKeyWrapper::is_started)
        .def("get_flags",
             [](TermKeyWrapper &tk) {
                 return interpret_flags(tk.get_flags(), "TermKeyFlag");
             })
        .def("set_flags",
             [](TermKeyWrapper &tk, py::set newflags) {
                 tk.set_flags(combine_flags(newflags, "TermKeyFlag"));
             })
        .def("get_waittime",
             [](TermKeyWrapper &tk) { return tk.get_waittime(); })
        .def("set_waittime",
             [](TermKeyWrapper &tk, int msec) { tk.set_waittime(msec); })
        .def("get_canonflags",
             [](TermKeyWrapper &tk) {
                 return interpret_flags(tk.get_canonflags(), "TermKeyCanon");
             })
        .def(
            "set_canonflags",
            [](TermKeyWrapper &tk, py::set newcanonflags) {
                tk.set_canonflags(combine_flags(newcanonflags, "TermKeyCanon"));
            })
        .def("get_buffer_size", &TermKeyWrapper::get_buffer_size)
        .def("set_buffer_size", &TermKeyWrapper::set_buffer_size)
        .def("get_buffer_remaining", &TermKeyWrapper::get_buffer_remaining)
        .def("canonicalise", &TermKeyWrapper::canonicalise)
        .def("keycmp", &TermKeyWrapper::keycmp)
        .def("push_bytes", [](TermKeyWrapper &tk, string str) {
            tk.push_bytes(str.c_str(), str.length());
        });
    // currently unimplemented: mouse/cursor functions and some of the more
    // advanced key interpretation functions

    py::class_<TermKeyKey>(m, "TermKeyKey")
        .def("type", [](TermKeyKey &key) { return key.type; })
        .def("code",
             [](TermKeyKey &key) {
                 switch (key.type) {
                     case TERMKEY_TYPE_UNICODE:
                         return py::cast(key.code.codepoint);
                     case TERMKEY_TYPE_FUNCTION:
                         return py::cast(key.code.number);
                     case TERMKEY_TYPE_KEYSYM:
                         return py::cast(key.code.sym);
                     case TERMKEY_TYPE_MOUSE:
                         return py::cast(key.code.mouse);
                     default:
                         throw std::runtime_error("Unknown TermKeyKey type");
                 }
             })
        .def("modifiers", [](TermKeyKey &key) { return key.modifiers; })
        .def("utf8", [](TermKeyKey &key) { return key.utf8; });

    m.def("get_errno", []() { return errno; });

    m.def("set_errno", [](int err) { errno = err; });

    py::enum_<TermKeySym>(m, "TermKeySym")
        .value("UNKNOWN", TERMKEY_SYM_UNKNOWN)
        .value("NONE", TERMKEY_SYM_NONE)
        .value("BACKSPACE", TERMKEY_SYM_BACKSPACE)
        .value("TAB", TERMKEY_SYM_TAB)
        .value("ENTER", TERMKEY_SYM_ENTER)
        .value("ESCAPE", TERMKEY_SYM_ESCAPE)
        .value("SPACE", TERMKEY_SYM_SPACE)
        .value("DEL", TERMKEY_SYM_DEL)
        .value("UP", TERMKEY_SYM_UP)
        .value("DOWN", TERMKEY_SYM_DOWN)
        .value("LEFT", TERMKEY_SYM_LEFT)
        .value("RIGHT", TERMKEY_SYM_RIGHT)
        .value("BEGIN", TERMKEY_SYM_BEGIN)
        .value("FIND", TERMKEY_SYM_FIND)
        .value("INSERT", TERMKEY_SYM_INSERT)
        .value("DELETE", TERMKEY_SYM_DELETE)
        .value("SELECT", TERMKEY_SYM_SELECT)
        .value("PAGEUP", TERMKEY_SYM_PAGEUP)
        .value("PAGEDOWN", TERMKEY_SYM_PAGEDOWN)
        .value("HOME", TERMKEY_SYM_HOME)
        .value("END", TERMKEY_SYM_END)
        .value("CANCEL", TERMKEY_SYM_CANCEL)
        .value("CLEAR", TERMKEY_SYM_CLEAR)
        .value("CLOSE", TERMKEY_SYM_CLOSE)
        .value("COMMAND", TERMKEY_SYM_COMMAND)
        .value("COPY", TERMKEY_SYM_COPY)
        .value("EXIT", TERMKEY_SYM_EXIT)
        .value("HELP", TERMKEY_SYM_HELP)
        .value("MARK", TERMKEY_SYM_MARK)
        .value("MESSAGE", TERMKEY_SYM_MESSAGE)
        .value("MOVE", TERMKEY_SYM_MOVE)
        .value("OPEN", TERMKEY_SYM_OPEN)
        .value("OPTIONS", TERMKEY_SYM_OPTIONS)
        .value("PRINT", TERMKEY_SYM_PRINT)
        .value("REDO", TERMKEY_SYM_REDO)
        .value("REFERENCE", TERMKEY_SYM_REFERENCE)
        .value("REFRESH", TERMKEY_SYM_REFRESH)
        .value("REPLACE", TERMKEY_SYM_REPLACE)
        .value("RESTART", TERMKEY_SYM_RESTART)
        .value("RESUME", TERMKEY_SYM_RESUME)
        .value("SAVE", TERMKEY_SYM_SAVE)
        .value("SUSPEND", TERMKEY_SYM_SUSPEND)
        .value("UNDO", TERMKEY_SYM_UNDO)
        .value("KP0", TERMKEY_SYM_KP0)
        .value("KP1", TERMKEY_SYM_KP1)
        .value("KP2", TERMKEY_SYM_KP2)
        .value("KP3", TERMKEY_SYM_KP3)
        .value("KP4", TERMKEY_SYM_KP4)
        .value("KP5", TERMKEY_SYM_KP5)
        .value("KP6", TERMKEY_SYM_KP6)
        .value("KP7", TERMKEY_SYM_KP7)
        .value("KP8", TERMKEY_SYM_KP8)
        .value("KP9", TERMKEY_SYM_KP9)
        .value("KPENTER", TERMKEY_SYM_KPENTER)
        .value("KPPLUS", TERMKEY_SYM_KPPLUS)
        .value("KPMINUS", TERMKEY_SYM_KPMINUS)
        .value("KPMULT", TERMKEY_SYM_KPMULT)
        .value("KPDIV", TERMKEY_SYM_KPDIV)
        .value("KPCOMMA", TERMKEY_SYM_KPCOMMA)
        .value("KPPERIOD", TERMKEY_SYM_KPPERIOD)
        .value("KPEQUALS", TERMKEY_SYM_KPEQUALS)
        .value("N_SYMS", TERMKEY_N_SYMS);

    py::enum_<TermKeyType>(m, "TermKeyType")
        .value("UNICODE", TERMKEY_TYPE_UNICODE)
        .value("FUNCTION", TERMKEY_TYPE_FUNCTION)
        .value("KEYSYM", TERMKEY_TYPE_KEYSYM)
        .value("MOUSE", TERMKEY_TYPE_MOUSE)
        .value("POSITION", TERMKEY_TYPE_POSITION)
        .value("MODEREPORT", TERMKEY_TYPE_MODEREPORT)
        .value("DCS", TERMKEY_TYPE_DCS)
        .value("OSC", TERMKEY_TYPE_OSC)
        .value("UNKNOWN_CSI", TERMKEY_TYPE_UNKNOWN_CSI);

    py::enum_<TermKeyResult>(m, "TermKeyResult")
        .value("NONE", TERMKEY_RES_NONE)
        .value("KEY", TERMKEY_RES_KEY)
        .value("EOF", TERMKEY_RES_EOF)
        .value("AGAIN", TERMKEY_RES_AGAIN)
        .value("ERROR", TERMKEY_RES_ERROR);

    py::enum_<TermKeyMouseEvent>(m, "TermKeyMouseEvent")
        .value("UNKNOWN", TERMKEY_MOUSE_UNKNOWN)
        .value("PRESS", TERMKEY_MOUSE_PRESS)
        .value("DRAG", TERMKEY_MOUSE_DRAG)
        .value("RELEASE", TERMKEY_MOUSE_RELEASE);

    py::enum_<TermKeyKeyMod>(m, "TermKeyKeyMod")
        .value("SHIFT", TermKeyKeyMod::SHIFT)
        .value("ALT", TermKeyKeyMod::ALT)
        .value("CTRL", TermKeyKeyMod::CTRL);

    py::enum_<TermKeyFlag>(m, "TermKeyFlag")
        .value("NOINTERPRET", TermKeyFlag::NOINTERPRET)
        .value("CONVERTKP", TermKeyFlag::CONVERTKP)
        .value("RAW", TermKeyFlag::RAW)
        .value("UTF8", TermKeyFlag::UTF8)
        .value("NOTERMIOS", TermKeyFlag::NOTERMIOS)
        .value("SPACESYMBOL", TermKeyFlag::SPACESYMBOL)
        .value("CTRLC", TermKeyFlag::CTRLC)
        .value("EINTR", TermKeyFlag::_EINTR)
        .value("NOSTART", TermKeyFlag::NOSTART);

    py::enum_<TermKeyCanon>(m, "TermKeyCanon")
        .value("SPACESYMBOL", TermKeyCanon::SPACESYMBOL)
        .value("DELBS", TermKeyCanon::DELBS);

    py::enum_<TermKeyFormat>(m, "TermKeyFormat")
        .value("LONGMOD", TERMKEY_FORMAT_LONGMOD)
        .value("CARETCTRL", TERMKEY_FORMAT_CARETCTRL)
        .value("ALTISMETA", TERMKEY_FORMAT_ALTISMETA)
        .value("WRAPBRACKET", TERMKEY_FORMAT_WRAPBRACKET)
        .value("SPACEMOD", TERMKEY_FORMAT_SPACEMOD)
        .value("LOWERMOD", TERMKEY_FORMAT_LOWERMOD)
        .value("LOWERSPACE", TERMKEY_FORMAT_LOWERSPACE)
        .value("MOUSE_POS", TERMKEY_FORMAT_MOUSE_POS)
        .value("VIM", TERMKEY_FORMAT_VIM)
        .value("URWID", TERMKEY_FORMAT_URWID);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
