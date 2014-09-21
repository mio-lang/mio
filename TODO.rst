TODO
====

Manually maintained ToDo List.


- Fix handling of constant/literal values being parsed, their bytecode
  and the way they are handled during runtime interpreter evaluation.

- Message tree rewriting.

  - ``a = 1`` --> ``setattr("x", 1)``
  - ``del a`` --> ``delattr("x")``

- Message tree operator shuffling

  - ``1 + 2 * 3`` -> ``(1 + (2 * 3))``

- Implement all bytecode instructions.
- Implement the runtime environment and core objects.
- Test Suite
- Documentation
- Examples
- Debugger
- Code Formatter
- Package Manager
