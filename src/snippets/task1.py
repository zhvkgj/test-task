from functools import wraps


def n_times(times):
    def deco(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)

        return inner

    return deco


@n_times(times=3)
def do_something():
    print("Something is going on!")


if __name__ == '__main__':
    do_something()
    # Something is going on!
    # Something is going on!
    # Something is going on!
