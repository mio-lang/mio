# -*- encoding: utf-8 -*-

from js.bytecode import to_code, ByteCode, \
    LOAD_CONSTANT_FLOAT, RETURN, JUMP_IF_FALSE, JUMP_ABSOLUTE
from js.interpreter import Frame, interpret, interpret_source
from js.base_objects import W_FloatObject, W_BoolObject


def test_frame():
    bc = ByteCode('', ['x', 'y'], [], [])
    frame = Frame(bc)
    assert len(frame.vars) == 2
    assert frame.valuestack_pos == 0
    x, y = object(), object()
    frame.push(x)
    assert frame.valuestack_pos == 1
    res = frame.pop()
    assert res is x
    assert frame.valuestack_pos == 0
    frame.push(x)
    frame.push(y)
    assert frame.valuestack_pos == 2
    res = frame.pop()
    assert res is y
    assert frame.valuestack_pos == 1


def test_load_constant():
    bc = ByteCode(to_code([
        LOAD_CONSTANT_FLOAT, 0,
        RETURN, 0]),
        [], [12.2], [])
    frame = interpret(bc)
    assert frame.test_valuestack == [W_FloatObject(12.2)]
    assert frame.vars == []


def test_assignment():
    frame = interpret_source('x = 2.71;')
    assert frame.test_valuestack == []
    assert frame.vars == [W_FloatObject(2.71)]


def test_load_variable():
    frame = interpret_source('''
    x = 2.71;
    y = x;
    ''')
    assert frame.test_valuestack == []
    assert frame.names == ['x', 'y']
    assert frame.vars == [W_FloatObject(2.71), W_FloatObject(2.71)]


def test_dicard_top():
    frame = interpret_source('2.71;')
    assert frame.test_valuestack == []
    assert frame.vars == []


def test_jumps():
    bc = ByteCode(to_code([
        LOAD_CONSTANT_FLOAT, 0,
        JUMP_IF_FALSE, 8,
        LOAD_CONSTANT_FLOAT, 1,
        JUMP_ABSOLUTE, 10,
        LOAD_CONSTANT_FLOAT, 2,
        RETURN, 0]),
        [], [0.0, -1.0, 1.0], [])
    frame = interpret(bc)
    assert frame.test_valuestack == [W_FloatObject(1.0)]

    bc = ByteCode(to_code([
        LOAD_CONSTANT_FLOAT, 0,
        JUMP_IF_FALSE, 8,
        LOAD_CONSTANT_FLOAT, 1,
        JUMP_ABSOLUTE, 10,
        LOAD_CONSTANT_FLOAT, 2,
        RETURN, 0]),
        [], [1.0, -1.0, 2.0], [])
    frame = interpret(bc)
    assert frame.test_valuestack == [W_FloatObject(-1.0)]


def test_if():
    frame = interpret_source('''
    if (0) {
        x = 10;
    }''')
    assert frame.names == ['x']
    assert frame.vars == [None]
    assert frame.test_valuestack == []

    frame = interpret_source('''
    if (1) {
        x = 10;
    }''')
    assert frame.names == ['x']
    assert frame.vars == [W_FloatObject(10.0)]
    assert frame.test_valuestack == []


def test_while():
    frame = interpret_source('''
    while (0) {
        x = 10;
    }''')
    assert frame.names == ['x']
    assert frame.vars == [None]
    assert frame.test_valuestack == []

    frame = interpret_source('''
    x = 1;
    y = 10;
    while (x) {
        x = 0;
        y = 100;
    }''')
    assert frame.names == ['x', 'y']
    assert frame.vars == [W_FloatObject(0.0), W_FloatObject(100.0)]
    assert frame.test_valuestack == []


def test_binary_add():
    frame = interpret_source('''
    x = 1 + 2.5;
    ''')
    assert frame.names == ['x']
    assert frame.vars == [W_FloatObject(3.5)]
    assert frame.test_valuestack == []


def test_binary_bool():
    for binary_op, check_fn in [
            ('<', lambda x, y: x < y),
            ('==', lambda x, y: x == y),
    ]:
        for x, y in [(1.0, 2.5), (1.0, 1.0), (1.0, 1.1)]:
            frame = interpret_source('''
            x = %s;
            y = %s;
            res = x %s y;
            ''' % (x, y, binary_op))
            assert frame.names == ['x', 'y', 'res']
            assert frame.vars == [
                W_FloatObject(x), W_FloatObject(y),
                W_BoolObject(check_fn(x, y))]
            assert frame.test_valuestack == []


def test_while_loops():
    frame = interpret_source('''
    x = 0;
    while (x < 10) {
        x = x + 1;
    }
    ''')
    assert frame.names == ['x']
    assert frame.vars == [W_FloatObject(10.0)]
    assert frame.test_valuestack == []


def test_print(capfd):
    frame = interpret_source('print(3.78);')
    out, _ = capfd.readouterr()
    assert out == '3.78\n'
    assert frame.test_valuestack == []


def test_arithmetic_expressions():
    frame = interpret_source('''
    x = 10;
    y = 4 + x * 2;
    z = (x + y) / x + 3;
    foo = y % 5 + y % 1 + y % 2;
    ''')
    x = 10.0
    y = 4 + x * 2
    z = (x + y) / x + 3
    foo = y % 5 + y % 1 + y % 2
    assert frame.names == ['x', 'y', 'z', 'foo']
    assert frame.vars == map(W_FloatObject, [x, y, z, foo])
    assert frame.test_valuestack == []


def test_fn_noop():
    frame = interpret_source('''
    function foo() {};
    foo();
    ''')
    assert frame.names == ['foo']
    assert len(frame.vars) == 1
    assert frame.test_valuestack == []


def test_fn_print(capfd):
    frame = interpret_source('''
    function foo() {
        print(1);
    };
    foo();
    ''')
    out, _ = capfd.readouterr()
    assert out == '1.0\n'
    assert frame.names == ['foo']
    assert len(frame.vars) == 1
    assert frame.test_valuestack == []


def test_fn_args(capfd):
    frame = interpret_source('''
    function foo(x) {
        print(x);
    };
    foo(10);
    ''')
    out, _ = capfd.readouterr()
    assert out == '10.0\n'
    assert frame.names == ['foo']
    assert len(frame.vars) == 1
    assert frame.test_valuestack == []

    frame = interpret_source('''
    function foo(x, y) {
        print(x + y);
    };
    x = 20;
    foo(10, x);
    ''')
    out, _ = capfd.readouterr()
    assert out == '30.0\n'
    assert frame.names == ['foo', 'x']
    assert len(frame.vars) == 2
    assert frame.test_valuestack == []


def test_return():
    frame = interpret_source('''
    function const() {
        return 3.14;
    };
    z = const();
    ''')
    assert frame.names == ['const', 'z']
    assert frame.vars[1] == W_FloatObject(3.14)

    frame = interpret_source('''
    function two(x) {
        return x * 2;
    };
    z = two(two(11));
    ''')
    assert frame.names == ['two', 'z']
    assert frame.vars[1] == W_FloatObject(44)


def test_scope():
    frame = interpret_source('''
    x = 10;
    function s() {
        return x;
    };
    y = s();
    ''')
    assert frame.names == ['x', 's', 'y']
    assert frame.vars[2] == W_FloatObject(10.0)

    frame = interpret_source('''
    g = 30;
    function s() {
        g = 10;
        function inner() {
            return g;
        };
        return inner;
    };
    function scoped() {
        g = 20;
        inner = s();
        return inner();
    };

    y = scoped();
    ''')
    assert frame.names == ['g', 's', 'scoped', 'y']
    assert frame.vars[3] == W_FloatObject(10.0)


def test_recursion():
    frame = interpret_source('''
    function fib(x) {
        if (x < 3) {
            return 1;
        } else {
            return fib(x - 1) + fib(x - 2);
        }
    };
    f1 = fib(1);
    f2 = fib(2);
    f3 = fib(3);
    f4 = fib(4);
    f10 = fib(10);
    ''')
    assert frame.names == ['fib', 'f1', 'f2', 'f3', 'f4', 'f10']
    assert frame.vars[1] == W_FloatObject(1.0)
    assert frame.vars[2] == W_FloatObject(1.0)
    assert frame.vars[3] == W_FloatObject(2.0)
    assert frame.vars[4] == W_FloatObject(3.0)
    assert frame.vars[5] == W_FloatObject(55.0)
