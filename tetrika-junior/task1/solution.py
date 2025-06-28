import inspect
from functools import wraps


def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__
    parameters = sig.parameters

    param_annotations = {
        name: expected_type
        for name, expected_type in annotations.items()
        if name != 'return' and name in parameters
    }

    if not param_annotations:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        for name, expected_type in param_annotations.items():
            value = bound_args.arguments[name]
            if expected_type is int and type(value) is bool:
                raise TypeError(
                    f"Argument '{name}' must be int, not bool"
                )
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Argument '{name}' must be {expected_type.__name__}, "
                    f"not {type(value).__name__}"
                )
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
