<!---
Copyright (c) 2019 Michael Vilim

This file is part of the pylibtermkey library. It is currently hosted at
https://github.com/mvilim/pylibtermkey

pylibtermkey is licensed under the MIT license. A copy of the license can be
found in the root folder of the project.
-->

## pylibtermkey

[![PyPI Release](https://img.shields.io/pypi/v/pylibtermkey.svg)](https://pypi.org/project/pylibtermkey/)
[![Build Status](https://travis-ci.org/mvilim/pylibtermkey.svg?branch=master)](https://travis-ci.org/mvilim/pylibtermkey)

pylibtermkey is a set of Python bindings for [libtermkey](http://www.leonerd.org.uk/code/libtermkey/), a library for interpreting terminal input. [Other Python bindings](https://github.com/temoto/ctypes_libtermkey) are out of date and not easily installable. This project has a few differences:

* libtermkey is automatically built as part of this project
* pybind11 is used for easy binding 
* unit tests are included 
* precompiled wheels are built from this repo and available on PyPI

### Installation

To install from PyPI:

```
pip install pylibtermkey
```

### Example

A minimal example of obtaining a keystroke and printing the results:

```
import pylibtermkey_cpp as termkey
tk = termkey.TermKey()

res, key = self.tk.waitkey()
print(res)
print(self.tk.strfkey(key, termkey.TermKeyFormat.VIM)
```

Note that, by default, termkey will read from stdin causing python terminal to not display typed characters. It is best to use termkey in an pre-written script rather in a REPL setup (as you will not be able to see what you are typing once termkey is active).

For other features, see the [tests](https://github.com/mvilim/pylibtermkey/blob/master/python/pylibtermkey/test_pylibtermkey.py) or the [libtermkey man pages](http://www.leonerd.org.uk/code/libtermkey/doc/).

### Building

To build this project:

Building from source requires cmake (`pip install cmake`).

```
python setup.py
```

### Unit tests

To run the unit tests:

```
python setup.py test
```

or use nose:

```
nosetests python/pylibtermkey
```

### Licensing

This project is licensed under the [MIT license](https://github.com/mvilim/pylibtermkey/blob/master/LICENSE). It uses the [pybind11](https://github.com/pybind/pybind11/) and [libtermkey](http://www.leonerd.org.uk/code/libtermkey/) projects whose licenses can be found in those [projects' directories](https://github.com/mvilim/pylibtermkey/blob/master/cpp/thirdparty).
