from __future__ import absolute_import, division, print_function

from collections import OrderedDict, defaultdict
from itertools import repeat

import dask
import toolz as t
import toolz.curried as tc
import cytoolz.curried as cyt

import daskfunk.utils as u
from daskfunk.compatibility import getargspec


_UNSPECIFIED = '::unspecified::'
_AMBIGUOUS = '::ambiguous::'
def _is_required(default):
    return default == _UNSPECIFIED or default == _AMBIGUOUS


def _func_param_info(argspec):
    params = argspec.args
    defaults = argspec.defaults or []
    start_default_ix = -max(len(defaults), 1) - 1
    values = [_UNSPECIFIED] * (len(params) - len(defaults)) + \
             list(defaults[start_default_ix:])
    return OrderedDict(zip(params, values))


def _is_curry_func(f):
    """
    Checks if f is a toolz or cytoolz function by inspecting the available attributes.
    Avoids explicit type checking to accommodate all versions of the curry fn.
    """
    return hasattr(f, 'func') and hasattr(f, 'args') and hasattr(f, 'keywords')


def _param_info(f):
    if _is_curry_func(f):
        argspec = getargspec(f.func)
        num_args = len(f.args)
        args_to_remove = argspec.args[0:num_args] + list(f.keywords.keys())
        base = _func_param_info(argspec)
        return t.dissoc(base, *args_to_remove)
    return(_func_param_info(getargspec(f)))


def compile(fn_graph, get=dask.get):
    fn_param_info = t.valmap(_param_info, fn_graph)
    global_param_info = {}
    for param_info in fn_param_info.values():
        for kw, value in param_info.items():
            if kw in global_param_info and global_param_info[kw] != value:
                global_param_info = _AMBIGUOUS
            else:
                global_param_info[kw] = value
    computed_args = set(fn_graph.keys())
    required_params, defaulted = u.split_keys_by_val(_is_required,
                                                     global_param_info)
    required_params = required_params - computed_args

    all_params = required_params.union(defaulted)
    default_args = u.select_keys(global_param_info, defaulted)

    def to_task(res_key, param_info):
        fn = fn_graph[res_key]
        args = tuple([default_args.get(p, p) for p in param_info.keys()])
        # this wrapper fn is needed to all args can be passed as
        # kargs, see test_graph_with_curried_fn_with_later_kwarg_provided
        # for motivation
        def wrapper(*args):
            kwargs = dict(zip(param_info.keys(), args))
            return fn(**kwargs)
        task = (wrapper,) + args
        return task

    base_dask = {k:to_task(k, param_info)
                 for k, param_info in fn_param_info.items()}

    outputs = list(fn_graph.keys())

    def funk(get=get, **kargs):
        param_keys = set(kargs.keys())
        missing_keys = required_params - param_keys
        if missing_keys:
            raise TypeError(
                'missing these keyword arguments: {}'.format(missing_keys))
        extra_keys = param_keys - all_params
        if extra_keys:
            raise TypeError(
                'unexpected keyword arguments passed in: {}'.format(extra_keys))

        dsk = t.merge(base_dask, default_args, kargs)
        res = get(dsk, outputs)
        return dict(zip(outputs, res))

    funk.required = required_params
    funk.defaults = default_args
    funk.base_dask = base_dask
    funk.full_dask = t.merge(base_dask,
                             dict(zip(all_params,
                                      repeat(_UNSPECIFIED))))

    return funk
