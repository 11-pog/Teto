import inspect

from typing import Any, Callable, Mapping, TypeVar, cast

def is_class_instance(parameters: Mapping[str, inspect.Parameter]) -> bool:
    first: inspect.Parameter|None = next(iter(parameters.values()), None)
    
    if (first is not None):
        return first.name == 'self'
    return False

F = TypeVar("F", bound=Callable[..., Any])

def get_original_func(func: F) -> F:
    out_func = func
    
    while hasattr(out_func, '__wrapped__'):
        out_func = cast(F, getattr(out_func, '__wrapped__'))
    
    return out_func