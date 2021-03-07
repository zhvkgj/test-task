from functools import wraps


def static_variable(key, value):
    def deco(func):
        setattr(func, key, value)
        return func

    return deco


def register(func):
    depends_on.__pool[func.__name__] = func
    func.__depends_on = []
    return func


@static_variable("__pool", {})
def depends_on(list_funcs):
    def deco(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for fun_name in list_funcs:
                if fun_name not in depends_on.__pool:
                    raise ValueError(f"Dependency {fun_name} is not registered!")

            visited = set()
            to_go = [func.__name__]
            while to_go:
                cur = to_go.pop()
                if cur in visited:
                    raise RuntimeError("Cyclic reference!")
                visited.add(cur)
                for fun in reversed(depends_on.__pool[cur].__depends_on):
                    to_go.append(fun)

            for fun_name in inner.__depends_on:
                depends_on.__pool[fun_name]()

            return func(*args, **kwargs)

        inner.__depends_on = list_funcs
        depends_on.__pool[inner.__name__] = inner

        return inner

    if list_funcs:
        return deco
    return lambda x: x


@depends_on(["buzz"])
def do_something():
    print("doing something")


@depends_on(["fizz"])
def foo():
    print("foo")


@depends_on(["buzz"])
def fizz():
    print("fizz")


@register
def buzz():
    print("buzz")


@depends_on(["do_something", "foo"])
def do_other_thing():
    print("doing other thing")


if __name__ == '__main__':
    do_other_thing()
    # do_something()
    # doing other thing
