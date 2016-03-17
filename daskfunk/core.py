from __future__ import absolute_import, division, print_function

from collections import OrderedDict
from itertools import repeat

import dask.core as dc
import toolz as t
import toolz.curried as tc

import daskfunk.utils as u
from daskfunk.compatibility import getargspec


_UNSPECIFIED = '::unspecified::'
def _is_required(defaults):
    return len(defaults) > 1 or _UNSPECIFIED in defaults


def _param_info(argspec):
    params = argspec.args
    defaults = argspec.defaults or []
    start_default_ix = -max(len(defaults), 1) - 1
    values = [_UNSPECIFIED] * (len(params) - len(defaults)) + \
             list(defaults[start_default_ix:])
    return OrderedDict(zip(params, values))


def compile(fn_graph, get=dc.get):
    fn_param_info = t.valmap(t.compose(_param_info, getargspec), fn_graph)
    global_param_info = t.merge_with(set, *fn_param_info.values())
    computed_args = set(fn_graph.keys())
    required_params, defaulted = u.split_keys_by_val(_is_required,
                                                     global_param_info)
    required_params = required_params - computed_args

    all_params = required_params.union(defaulted)
    default_args = t.thread_last(defaulted,
                                 u.select_keys(global_param_info),
                                 tc.valmap(lambda set: list(set)[0]))

    def to_task(res_key, param_info):
        fn = fn_graph[res_key]
        args = tuple([default_args.get(p, p) for p in param_info.keys()])
        task = (fn,) + args
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
