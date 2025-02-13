import inspect

def represent(obj, detailed=True):
    cls = type(obj)

    if isinstance(obj, type):
        if obj.__module__ != 'builtins': return f"{obj.__module__}.{obj.__qualname__}"
    else:
        if getattr(obj, '__module__', 'builtins') != 'builtins' and cls.__repr__ == object.__repr__:
            return f"{(getattr(cls, '__module__', '') + '.') if detailed else ''}{cls.__name__}({hex(id(obj))})"
    
    try: return repr(obj)
    except: return f"{(getattr(cls, '__module__', '') + '.') if detailed else ''}{cls.__name__}({hex(id(obj))})"

def irepr(*args, **kwargs):
    sargs = ([represent(args[0], False)] + [represent(a) for a in args[1:]]) if args else []
    return ', '.join(sargs + [f"{k}={represent(v)}" for k, v in kwargs.items()])

def HOOK(clazz, bLog=True, _name=None):
    def decorator(func, _name=_name):
        name = func.__name__
        _name = _name or '_' + name
        
        original = getattr(clazz, name)
        # original = getattr(clazz, _name, getattr(clazz, name))
        setattr(clazz, _name, original)
        
        import functools
        @functools.wraps(original)
        def wrapper(*args, **kwargs):
            try:
                if bLog: print(f"HENTR: {clazz.__name__}.{name}({irepr(*args, **kwargs)})")
                
                # if not inspect.ismethod(original) and inspect.isfunction(original): result = func(clazz, *args, **kwargs)
                result = func(*args, **kwargs)
                
                if bLog: print(f"HEXIT: [bold magenta]{clazz.__name__}.{name}[/bold magenta] -> {represent(result)}")
                return result
            except: print(__import__('traceback').format_exc())
        
        setattr(clazz, name, wrapper)
        return func
    return decorator

def LOGC(clazz, exclude_methods=None):
    import inspect, types, traceback
    from functools import wraps
    
    exclude_methods = set(exclude_methods or ''.split('.'))
    
    for name in clazz.__dict__:
        if name in exclude_methods or (name != '__init__' and name.startswith('__')): continue

        attr = clazz.__dict__[name]

        if not isinstance(attr, (classmethod, staticmethod, types.FunctionType)): continue

        original_func = attr.__func__ if isinstance(attr, (classmethod, staticmethod)) else attr
        cm = isinstance(attr, classmethod)
        sm = isinstance(attr, staticmethod)
        is_async = inspect.iscoroutinefunction(original_func)
        
        def create_wrapper(func, name, cm, sm, is_async):
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    print(f"ENTR: {clazz.__name__}.{name}({irepr(*args, **kwargs)})")

                    result = func(*args, **kwargs)
                    
                    print(f"EXIT: [bold magenta]{clazz.__name__}.{name}[/bold magenta] -> {represent(result)}")
                    return result
                except Exception as e:
                    print(traceback.format_exc())
                    print(f"ERRR in {clazz.__name__}.{name}: {str(e)}")
                    raise

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    print(f"ENTR_ASYNC: {clazz.__name__}.{name}({irepr(*args, **kwargs)})")

                    result = await func(*args, **kwargs)
                    
                    print(f"EXIT_ASYNC: [bold magenta]{clazz.__name__}.{name}[/bold magenta] -> {represent(result)}")
                    return result
                except Exception as e:
                    print(traceback.format_exc())
                    print(f"ERRR_ASYNC in {clazz.__name__}.{name}: {str(e)}")
                    raise

            return async_wrapper if is_async else sync_wrapper

        wrapper = create_wrapper(original_func, name, cm, sm, is_async)

        if cm: setattr(clazz, name, classmethod(wrapper))
        elif sm: setattr(clazz, name, staticmethod(wrapper))
        else: setattr(clazz, name, wrapper)

def LOGM(module, exclude_clazz=None, blab=False):
    import inspect
    exclude_clazz = set(exclude_clazz or 'Singleton.enum.StoryTick'.split('.'))
    for name, clazz in inspect.getmembers(module, inspect.isclass):
        if name in exclude_clazz: continue
        if blab:
            if clazz.__module__ != getattr(module, '__name__', clazz.__module__): continue
        LOGC(clazz)

def LOG(obj):
    LOGM(obj)
    LOGC(obj)
