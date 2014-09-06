.. _Python: https://www.python.org/
.. _virtualenv: https://pypy.python.org/pypi/virtualenv
.. _virtualenvwrapper: https://pypy.python.org/pypi/virtualenvwrapper


Minimal I/O Interpreter
=======================

This is a minimal I/O Interpreter.


Prerequisites
-------------

It's recommended that you do all development using a Python Virtual
Environment using `virtualenv`_ and/or using the nice `virtualenvwrapper`_.

::
   
    $ mkvirtualenv mio

You will need the `RPython <https://bitbucket.org/pypy/pypy>`_ toolchain
to build the interpreter. The easiest way to do this is to
`My Fork of PyPy <https://bitbucket.org/prologic/pypy>`_ which includes
a convenient ``setup-rpython.py`` to make working with the RPython toolchain
a bit easier.

::
    
    $ hg clone https://bitbucket.org/prologic/pypy
    $ cd pypy
    $ python setup-rpython.py develop


Installation
------------

Grab the source from https://bitbucket.org/prologic/mio and either
run ``python setup.py develop`` or ``pip install -r requirements.txt``

::
    
    $ hg clone https://bitbucket.org/prologic/mio
    $ cd mio
    $ pip install -r requirements.txt


Building
--------

To build the interpreter simply run ``mio/main.py`` against the RPython
Compiler.

::
    
    $ rpython mio/main.py


Usage
-----

You can either run the interpreter using `Python`_ itself or running the
compiled interpreter ``mio``.

::
    
    $ mio examples/fib.mio
    $ ./bin/mio examples/fib.mio
