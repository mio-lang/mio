.. _Python: https://www.python.org/
.. _virtualenv: https://pypy.python.org/pypi/virtualenv
.. _virtualenvwrapper: https://pypy.python.org/pypi/virtualenvwrapper
.. _Docker: https://docker.com/
.. _fig: http://www.fig.sh/


Minimal I/O Interpreter
=======================

.. image:: https://drone.io/bitbucket.org/miolang/mio/status.png
   :target: https://drone.io/bitbucket.org/miolang/mio
   :alt: Drone.io Build Status

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

Grab the source from https://bitbucket.org/miolang/mio and either
run ``python setup.py develop`` or ``pip install -r requirements.txt``

::
    
    $ hg clone https://bitbucket.org/miolang/mio
    $ cd mio
    $ pip install -r requirements.txt


Building
--------

To build the interpreter simply run ``mio/main.py`` against the RPython
Compiler. There is a ``Makefile`` that has a default target for building
and translating the interpreter.

::
    
    $ make

As of `690c894 <https://bitbucket.org/miolang/mio/commits/690c894>`_ you can
now build mio using `Docker`_ and `fig`_.

::
    
    $ fig build


Usage
-----

You can either run the interpreter using `Python`_ itself or by running the
compiled interpreter ``mio`` in ``./bin/mio``.

::
    
    $ ./bin/mio examples/hello.mio

Untranslated running on top of `Python`_ (*CPython*):

::
    
    $ miopy examples/hello.mio

As of `690c894 <https://bitbucket.org/miolang/mio/commits/690c894>`_ you can
now run mio using `Docker`_ and `fig`_.

::
    
    $ fig run mio hello.mio
