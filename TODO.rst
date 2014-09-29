TODO
====

Manually maintained ToDo List.


- Message tree rewriting.

  - ``a = 1``       --> ``set("x", 1)``
  - ``return 1``    --> ``return(1)``
  - ``delete a``    --> ``delete("x")``

- Message tree operator shuffling

  - ``1 + 2 * 3``   --> ``(1 + (2 * 3))``
  - ``(1 + 2) * 3`` --> ``((1 + 2) * 3)``
