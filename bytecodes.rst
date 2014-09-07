mio Bytecode Insutrction Set
============================

- ``LOAD <value>``
  Load a constant value onto the stack (number, string, identifier).

- ``PUSH [<name>]``
  Push an optionally named message onto the stack popping all items on the
  stack as arguments for the message.

- ``GET <name>``
  Get the named attribute on the current context.

- ``SET <name> <value>``
  Set the named attribute to value on the current context.

- ``NEW``
  Clone the current context and create a new object setting the newly
  created object as the new context.

- ``EVAL``
  Evaluate the message on the top of the stack setting the context to
  the result of the evaluation.

- ``PUSHF``
  Push the current frame on to the stack. (*Continuations*)

- ``POPF``
  Pop frame off the top of the stack. (*Continuations*)

- ``END``
  Terminate the interpreter.
