from functools import wraps


def trace_if(pred):
    def deco(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if pred(*args, **kwargs):
                print(f"{func.__name__} {args} {kwargs}")
            return func(*args, **kwargs)

        return inner

    return deco


@trace_if(lambda x, y, **kwargs: kwargs.get("integral"))
def div(x, y, integral=False):
    return x // y if integral else x / y


if __name__ == '__main__':
    print(div(4, 2))
    # 2
    print(div(4, 2, integral=True))
    # div (4, 2) {'integral': True}
    # 2
