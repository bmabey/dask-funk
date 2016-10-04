==========
dask-funk
==========

.. image:: https://travis-ci.org/Savvysherpa/dask-funk.svg?branch=master
    :target: https://travis-ci.org/Savvysherpa/dask-funk

dask-funk provides an extension to dask_ that creates keyword named functions
(hence the funk!) from dasks_ or function graphs represented as dictionaries.
It is inspired by Plumatic's wonderful Graph_ library for clojure.

.. _dask: http://dask.pydata.org/en/latest/#
.. _dasks: http://dask.pydata.org/en/latest/spec.html
.. _Graph: https://github.com/plumatic/plumbing#graph-the-functional-swiss-army-knife

Example
=======


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

Installation
============


.. code:: bash

    conda install dask-funk

    or

    pip install dask-funk


Please fix or point out any errors, inaccuracies or typos you notice.
