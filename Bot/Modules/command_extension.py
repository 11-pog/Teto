import functools
from Modules.utils import IterUtils, StringUtils
import inspect




async def _send_if_msg(ctx, msg):
    if msg:
        await ctx.send(msg)



def is_class_instance(parameters):
    first = next(iter(parameters.values()), None)
    return first.name == 'self'



def get_original_func(func):
    out_func = func
    
    while hasattr(out_func, '__wrapped__'):
        out_func = out_func.__wrapped__
    
    return out_func



def command_extension(*extensions):
    extensions = IterUtils.for_each_item(
        extensions,
        StringUtils.clean,
        lambda phrase: phrase.split(' ')
        )
    min_extension_size = IterUtils.get_smallest_size(extensions)
    
    
    def decorator(func):
        original_func = get_original_func(func)
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
        
        
        async def _return_func_no_keyword(func, self, ctx, *words):
            args = [self, ctx, *words[:relevant_positional_args_amount]]
            return await func(*args)
        
        async def _return_func_keyword(func, self, ctx, *words):
            words_args = words[:relevant_positional_args_amount]
            kwargs = {
                keyword_arg.name: ' '.join(words[relevant_positional_args_amount:])
                }
            args = [self, ctx, *words_args]
            return await func(*args, **kwargs)
        
        def _build_return_function(positional_args_amount, has_keyword):
            if not has_keyword:
                return _return_func_no_keyword
            
            return _return_func_keyword
        
        return_function = _build_return_function(relevant_positional_args_amount, keyword_arg)
        
        #Wrapper
        async def wrapper(self, ctx, *words, **kwargs):
            if len(words) < min_extension_size:
                return
            
            is_match = False
            
            for extension in extensions:
                try:
                    is_match = all(words[index] == StringUtils.clean(word) for index, word in enumerate(extension))
                except ValueError:
                    pass
                
                if is_match:
                    return await return_function(func, self, ctx, *words[len(extension):])
        return wrapper
    return decorator