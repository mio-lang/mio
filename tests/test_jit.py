# -*- encoding: utf-8 -*-

from js import parser
from js.bytecode import LOAD_VAR, LOAD_CONSTANT_FLOAT, \
    CALL, LOAD_CONSTANT_FN, ASSIGN, DISCARD_TOP, RETURN, BINARY_ADD, \
    CompilerContext, to_code
from js.interpreter import get_printable_location


def test_get_location():
    filename = '_for_test_jit.js'
    source = '''
    function foo(x, y) {
        return x + y;
    };
    x = 3;
    foo(1, x);
    '''
    ast = parser.parse(source, filename=filename)
    bc = CompilerContext.compile_ast(ast, co_filename=filename)
    assert bc.code == to_code([
        LOAD_CONSTANT_FN, 0,
        ASSIGN, 0,
        LOAD_CONSTANT_FN, 0,
        DISCARD_TOP, 0,
        LOAD_CONSTANT_FLOAT, 0,
        ASSIGN, 1,
        LOAD_VAR, 0,
        LOAD_CONSTANT_FLOAT, 1,
        LOAD_VAR, 1,
        CALL, 2,
        DISCARD_TOP, 0,
        RETURN, 0])
    assert bc.co_name == '__main__'
    assert bc.co_filename == '_for_test_jit.js'
    assert bc.co_firstlineno == 0
    inner_bc = bc.constants_fn[0]
    assert inner_bc.code == to_code([
        LOAD_VAR, 0,
        LOAD_VAR, 1,
        BINARY_ADD, 0,
        RETURN, 1])
    assert inner_bc.co_name == 'foo'
    assert inner_bc.co_filename == '_for_test_jit.js'
    assert inner_bc.co_firstlineno == 1
    assert get_printable_location(0, bc.code, bc) == \
        "<code object __main__, file '_for_test_jit.js', line 1> #0 LOAD_CONSTANT_FN"
    assert get_printable_location(2, bc.code, bc) == \
        "<code object __main__, file '_for_test_jit.js', line 1> #2 ASSIGN"
    assert get_printable_location(0, inner_bc.code, inner_bc) == \
        "<code object foo, file '_for_test_jit.js', line 2> #0 LOAD_VAR"
    assert get_printable_location(4, inner_bc.code, inner_bc) == \
        "<code object foo, file '_for_test_jit.js', line 2> #4 BINARY_ADD"
