def process_import(name):
    return f"import {name}\n"

def process_variable(name, value, annotation = None):
    annotation = annotation or type(value)
    return f"{name}: {annotation.__name__} = {repr(value)}\n"

def process_function(func, name = None):
    name = name or func.__name__
    sig = __import__('inspect').signature(func)
    return f"{'async ' if __import__('inspect').iscoroutinefunction(func) else ''}def {name}{str(sig)}: {'yield ' if __import__('inspect').isgeneratorfunction(func) else ''}...\n"

def process_class(clazz, class_name = None):
    class_name = class_name or clazz.__name__
    bases = [base.__name__ for base in clazz.__bases__]
    bases = f"({', '.join(bases)})" if bases else ''
    _ = f"class {class_name}{bases}:\n"
    
    variables = []
    functions = []
    
    for name, method in __import__('inspect').getmembers(clazz):
        if name.startswith("__"): continue
        
        if __import__('inspect').isfunction(method) or __import__('inspect').ismethod(method):
            __ = ''
            if isinstance(method, staticmethod): __ = '    @staticmethod\n'
            elif isinstance(method, classmethod): __ = '    @classmethod\n'
            functions.append(f"{__}    {process_function(method, name)}")
        elif isinstance(method, property):
            functions.append(f"    @property\n    def {name}(self): ...")
        else: variables.append(f"    {process_variable(name, method)}")
    
    if variables: _ += ''.join(variables) + '\n'
    if functions: _ += ''.join(functions) + '\n'
    
    return _

processed = set()
def process_module(module):
    if id(module) in processed: return ''
    processed.add(id(module))
    
    _ = f"# module: {module.__name__}\n\n"
    
    annotations = getattr(module, "__annotations__", {})
    
    imports = []
    variables = []
    clazz = []
    functions = []

    for name, member in __import__('inspect').getmembers(module):
        if name.startswith("__"): continue
        
        if __import__('inspect').isclass(member): clazz.append(process_class(member, name))
        elif __import__('inspect').isfunction(member) or __import__('inspect').ismethod(member): functions.append(process_function(member, name))
        elif __import__('inspect').ismodule(member):
            try:
                if 'com.netease.newspikeme' in member.__file__:
                    __import__('os').makedirs(member.__file__.rsplit('/', 1)[0], exist_ok=True)
                    newdata = process_module(member)
                    newsize = len(newdata.encode())
                    try: currentsize = __import__('os').path.getsize(member.__file__)
                    except FileNotFoundError: currentsize = 0
                    
                    if newsize > currentsize: open(member.__file__, 'w').write(newdata)
            except: pass
            
            imports.append(process_import(name))
        else: variables.append(process_variable(name, member, annotations.get(name)))
    
    if imports: _ += ''.join(imports) + '\n'
    if variables: _ += ''.join(variables) + '\n'
    if clazz: _ += ''.join(clazz) + '\n'
    if functions: _ += ''.join(functions) + '\n'
    
    return _

def process(_):
    if __import__('inspect').isclass(_): return process_class(_)
    elif __import__('inspect').isfunction(_) or __import__('inspect').ismethod(_): return process_function(_)
    elif __import__('inspect').ismodule(_): return process_module(_)
    else: return process_variable('idk', _)
