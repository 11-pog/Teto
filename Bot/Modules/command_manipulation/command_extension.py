import inspect
from typing import Any, Callable, Iterable

from Modules.utils import IterTools, StringTools
from Modules.command_manipulation._core import get_original_func


def command_extension(*extensions: str):
    extensions = tuple(IterTools.for_each_item(
        extensions,
        StringTools.clean,
        lambda phrase: phrase.split(' ')
        ))
    min_extension_size = IterTools.get_smallest_size(extensions)
    
    return _extension_decorator(extensions, min_extension_size)


def _extension_decorator(extensions: Iterable[str], min_extension_size: int | float):
    def decorator(func: Callable[..., Any]):
        original_func: Callable[..., Any] = get_original_func(func)
        signature = inspect.signature(original_func)
        parameters = signature.parameters
        
        relevant_positional_args_amount = len([
            param for param in parameters.values() 
            if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD)
        ]) - 2
        
        keyword_arg = None
        for param in parameters.values():
            if param.kind == param.KEYWORD_ONLY:
                keyword_arg = param
                break
        
        if not keyword_arg:
            async def _return_func(func, self, ctx, *words):
                args = [self, ctx, *words[:relevant_positional_args_amount]]
                return await func(*args)
        else:
            async def _return_func(func, self, ctx, *words):
                words_args = words[:relevant_positional_args_amount]
                kwargs = {
                    keyword_arg.name: ' '.join(words[relevant_positional_args_amount:])
                    }
                args = [self, ctx, *words_args]
                return await func(*args, **kwargs)
        
        async def wrapper(self, ctx, *words, **kwargs):
            if len(words) < min_extension_size:
                return
            
            is_match = False
            
            for extension in extensions:
                try:
                    is_match = all(words[index] == StringTools.clean(word) for index, word in enumerate(extension))
                except ValueError:
                    pass
                
                if is_match:
                    return await _return_func(func, self, ctx, *words[len(extension):])
        return wrapper
    return decorator