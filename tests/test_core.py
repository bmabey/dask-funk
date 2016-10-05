from collections import OrderedDict
import toolz as t
import cytoolz as cyt

import daskfunk.core as dfc
from daskfunk.compatibility import PY3


def inc(x):
   return x + 1


def test_compile():
    def load_data(filename):
        return [1,2,3]

    def process_data_A(data):
        return [i + 5 for i in data]

    def process_data_B(data):
        return [i + 10 for i in data]

    def combine_processed_data(filename, inc5, inc10):
        return filename, [a + b for a, b in zip(inc5, inc10)]

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

def test_defaults_can_be_overriden():

   def three_sum(a, b=5, c=5):
        return a + b + c

    # note how we specify b
   fn_graph = {'x': three_sum, 'inc': lambda x: x + 1}
   funk = dfc.compile(fn_graph)

   assert funk(a=1) == {'x': 11, 'inc': 12}
   assert funk(a=1,b=2,c=3) == {'x': 6, 'inc': 7}


def test_compile_with_unhashable_types_as_defaults():
    def load_data(filename):
        return [1,2,3]

    def process_data(data, opts={'foo': 42}, nums=set([4,5])):
        return [i + 5 for i in data]

    fn_graph = {'data': load_data,
                'inc5': process_data,}

    funk = dfc.compile(fn_graph)

    res = funk(filename='foo-bar')

    assert res == {'data': [1,2,3],
                   'inc5': [6, 7, 8]}


def test_intermediate_values_are_reused():
    times_loaded = {'total': 0}
    def load_data(filename):
      times_loaded['total'] += 1
      return [1,2,3]

    def process_data_A(data):
        return [i + 5 for i in data]

    def process_data_B(data):
        return [i + 10 for i in data]

    def combine_processed_data(filename, inc5, inc10):
        return filename, [a + b for a, b in zip(inc5, inc10)]

    fn_graph = {'data': load_data,
                'inc5': process_data_A,
                'inc10': process_data_B,
                'res': combine_processed_data}
    funk = dfc.compile(fn_graph)

    res = funk(filename='foo-bar')

    assert times_loaded['total'] == 1


def test_graph_with_curried_fn_with_later_kwarg_provided():
    @t.curry
    def three_sum(a, b=5, c=3):
       return a + b + c

    # note how we specify b
    fn_graph = {'x': three_sum(b=10),
                'inc': lambda x: x + 1}
    funk = dfc.compile(fn_graph)

    assert funk.required == set(('a'))
    assert funk.defaults == {'c': 3}

    assert funk(a=0) == {'x': 13,
                         'inc':14}

    assert funk(a=1, c=0) == {'x': 11,
                              'inc': 12}

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
