import collections
import functools
import unittest.mock


def lru_cache(*args, **kwargs):
    maxsize = kwargs.get("maxsize", 128)
    wrap_decorator = lru_cache_wrapper(maxsize)
    if args:
        return wrap_decorator(args[0])
    else:
        return wrap_decorator


def lru_cache_wrapper(maxsize):
    def lru_cache_decorator(func):
        cache = collections.OrderedDict()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = tuple(sorted(list(args) + list(kwargs.values())))
            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            if maxsize and len(cache) >= maxsize:
                cache.popitem(last=False)

            return result

        return wrapper

    return lru_cache_decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
