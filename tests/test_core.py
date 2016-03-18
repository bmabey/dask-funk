from collections import OrderedDict
import toolz as t
import cytoolz as cyt

import daskfunk.core as dfc

def load_data(filename):
    return [1,2,3]

def process_data_A(data):
    return [i + 5 for i in data]

def process_data_B(data):
    return [i + 10 for i in data]

def combine_processed_data(filename, inc5, inc10):
    return filename, [a + b for a, b in zip(inc5, inc10)]


def test_compile():
    fn_graph = {'data': load_data,
                'inc5': process_data_A,
                'inc10': process_data_B,
                'res': combine_processed_data}
    funk = dfc.compile(fn_graph)

    res = funk(filename='foo-bar')

    assert res == {'data': [1,2,3],
                   'inc5': [6, 7, 8],
                   'inc10': [11, 12, 13],
                   'res': ('foo-bar', [17, 19, 21])}


def test_param_info_regular_function():
    def foo(a, b, c='bar'):
        return a + b

    res = dfc._param_info(foo)
    assert res == OrderedDict([('a', '::unspecified::'),
                               ('b', '::unspecified::'),
                               ('c', 'bar')])

def test_param_info_curried_function():

    @t.curry
    def foo(a, b, c='bar'):
        return a + b

    res = dfc._param_info(foo)
    assert res == OrderedDict([('a', '::unspecified::'),
                               ('b', '::unspecified::'),
                               ('c', 'bar')])

def test_param_info_positional_curried_function():

    @t.curry
    def foo(a, b, c='bar'):
        return a + b

    myfoo = foo(5)
    res = dfc._param_info(myfoo)
    assert res == OrderedDict([('b', '::unspecified::'),
                               ('c', 'bar')])


def test_param_info_keyword_curried_function():

    @t.curry
    def foo(a, b, c='bar'):
        return a + b

    myfoo = foo(c='baz')

    res = dfc._param_info(myfoo)
    assert res == OrderedDict([('a', '::unspecified::'),
                               ('b', '::unspecified::')])


def test_param_info_nested_curried_function():

    @t.curry
    def foo(a, b, c='bar'):
        return a + b

    myfoo = foo(c='baz')
    another_foo = myfoo(55)

    res = dfc._param_info(another_foo)
    assert res == OrderedDict([('b', '::unspecified::')])

def test_param_info_with_cytoolz_curry():

    @cyt.curry
    def foo(a, b, c='bar'):
        return a + b

    myfoo = foo(c='baz')
    another_foo = myfoo(55)

    res = dfc._param_info(another_foo)
    assert res == OrderedDict([('b', '::unspecified::')])
