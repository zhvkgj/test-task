from functools import wraps
from inspect import getcallargs, getfullargspec
from collections import OrderedDict
from json import dumps


def cached(func=None, *, cache_size=None):
    def deco(fun):
        deco.cache = OrderedDict()

        if cache_size == 0:
            return fun
        else:
            @wraps(fun)
            def inner(*args, **kwargs):
                exec_info = getcallargs(fun, *args, **kwargs)
                varkw = getfullargspec(fun).varkw
                if varkw:
                    temp = exec_info[varkw]
                    exec_info.pop(varkw)
                    exec_info.update(temp)

                key = dumps(exec_info.items())
                if key in deco.cache:
                    deco.cache.move_to_end(key, last=True)
                else:
                    deco.cache[key] = fun(*args, **kwargs)

                if cache_size is not None and len(deco.cache) > cache_size:
                    deco.cache.popitem(last=False)

                return deco.cache[key]

        return inner

    if func is not None:
        return deco(func)

    return deco
