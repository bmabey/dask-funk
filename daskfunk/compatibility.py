import inspect
import sys

PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2


if PY3:
    def getargspec(func):
        return inspect.getfullargspec(func)
else:
    def getargspec(func):
        return inspect.getargspec(func)
