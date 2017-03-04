==========
dask-funk
==========
*random access DAGs*

.. image:: https://travis-ci.org/bmabey/dask-funk.svg?branch=master
    :target: https://travis-ci.org/bmabey/dask-funk

dask-funk provides an extension to dask_ that creates keyword named functions
(hence the funk!) from dasks_ or function graphs represented as dictionaries.
It is inspired by Plumatic's wonderful Graph_ library for clojure. Feature parity
with the clojure version is not 100% nor is that the goal for the foreseeable future.
This version is missing Schema-like support and doesn't work with sub-graphs.

.. _dask: http://dask.pydata.org/en/latest/#
.. _dasks: http://dask.pydata.org/en/latest/spec.html
.. _Graph: https://github.com/plumatic/plumbing#graph-the-functional-swiss-army-knife

Example
=======

Note how the ``inc`` function is "named" ``n`` in the dictionary and so the result
of ``inc``'s call is automatically fed into ``doubled`` which takes the ``n`` parameter:

.. code:: python

    >>> from operator import add

    >>> import daskfunk as dsf

    >>> inc = lambda x: x + 1
    >>> double = lambda n: n * 2
    >>> d = {'n': inc, 'doubled': double}
    >>> f = dsf.compile(d)
    >>> result = f(x=2)
    >>> result == {'n': 3, 'doubled': 6}
    True


Why?
=======

For motivation see the posts_ and docs for Plumatic's Graph_. Basically, it saves you from
having to wire up all of your functions yourself. For simple functions like above this is
silly but for complex pipelines this can save substantial time.

The big selling point of this library is that it rides on top of dask_. Which means
you can use any dask scheduler_ to run your function/pipeline/DAG (pass in a ``get``
to ``compile`` or when you run your funk). This becomes incredibly useful when you want
to run multiple steps of your pipeline in parallel. Since the DAG is all inferred from the
function parameters the work of kicking off parallel tasks is done automatically by dask!

.. _posts: https://plumatic.github.io//prismatics-graph-at-strange-loop
.. _scheduler: http://dask.pydata.org/en/latest/scheduler-overview.html


Trade-offs
=======

I've used this library and the original Graph_ in a number of projects. While useful there are some
drawbacks. The first one is that your pipeline is now opaque since it isn't explicitly defined in
your code, which is of course the whole point! This can be confusing to new comers to the project.
The compiled funks have dasks_ associated with them however than can be plotted with GraphViz which
is quite helpful in explaining what a funk is doing.

The other downside to this library is the static nature of the DAGs and how it requires you to keep
all of your parameter names consistent across functions. When this becomes painful I typically revert
to using bare dasks_ to implement my pipeline.


Installation
============


.. code:: bash

    conda install dask-funk

    or

    pip install dask-funk


Please fix or point out any errors, inaccuracies or typos you notice.
