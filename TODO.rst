TODO
====

Manually maintained ToDo List.


- Refactor Interpreter.
- Message tree rewriting.

  - ``a = 1``       --> ``set("x", 1)``
  - ``return 1``    --> ``return(1)``
  - ``del a``       --> ``delete("x")``

- Message tree operator shuffling

  - ``1 + 2``       --> ``1 +(2)``
  - ``1 + 2 * 3``   --> ``1 +(2 *(3))``
  - ``(1 + 2) * 3`` --> ``(1 +(2)) *(3)``
