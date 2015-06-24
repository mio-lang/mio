.. _Python: https://www.python.org/
.. _virtualenv: https://pypy.python.org/pypi/virtualenv
.. _virtualenvwrapper: https://pypy.python.org/pypi/virtualenvwrapper
.. _Docker: https://docker.com/
.. _Latest Build: https://drone.io/bitbucket.org/miolang/mio/files


Minimal I/O Interpreter
=======================

.. image:: https://travis-ci.org/mio-lang/mio.svg
   :target: https://travis-ci.org/mio-lang/mio
   :alt: Build Status

This is a minimal I/O Interpreter. This is a rewrite of:

- https://bitbucket.org/prologic/mio-lang


.. warning:: mio is a new programming language in early **Development**.

             DO NOT USE IN PRODUCTION!
             
             USE AT YOUR OWN RISK!


Prerequisites
-------------

It is recommended that you do all development using a Python Virtual
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
    $ python setup-pypy develop
    $ python setup-rpython.py develop


Installation
------------

Grab the source from https://github.com/mio-lang/mio and either
run ``python setup.py develop`` or ``pip install -r requirements.txt``

::
    
    $ git clone https://github.com/mio-lang/mio.git
    $ cd mio
    $ pip install -r requirements.txt

You can also download the `Latest Build`_


Building
--------

To build the interpreter simply run ``mio/main.py`` against the RPython
Compiler. There is a ``Makefile`` that has a default target for building
and translating the interpreter.

::
    
    $ make

You can also use `Docker`_ to build the interpreter:

::
    
    $ docker build -t mio .


Usage
-----

You can either run the interpreter using `Python`_ itself or by running the
compiled interpreter ``mio`` in ``./bin/mio``.

::
    
    $ ./bin/mio examples/hello.mio

Untranslated running on top of `Python`_ (*CPython*):

::
    
    $ miopy examples/hello.mio


Grammar
-------

The grammar of mio is currently as follows:

::
    
    program = expressions

    expressions = { expression }

    expression = message | terminator

    message = symbol | arguments | symbol arguments

    arguments = T_LPAREN arguments_list T_RPAREN |
                T_LBRACE arguments_list T_RBRACE |
                T_LBRACKET arguments_list T_RBRACKET

    arguments_list = expressions | expressions T_COMMA arguments_list

    symbol = T_IDENTIFIER | T_OPERATOR | T_NUMBER | T_STRING

    terminator = T_TERMINATOR
