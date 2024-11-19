# __init__.py

__version__ = '0.1.1'
__author__ = 'Long Jiang'

import pkgutil
import inspect
import sys

# Dynamically import all functions and classes from analyze_basin.py
from . import analyze_basin

# Add all functions and classes from analyze_basin to the module's namespace dynamically
for module_info in pkgutil.iter_modules(analyze_basin.__path__):
    module = __import__(f"{analyze_basin.__name__}.{module_info.name}", fromlist=[module_info.name])
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) or inspect.isclass(obj):
            setattr(sys.modules[__name__], name, obj)

__all__ = [name for name, obj in inspect.getmembers(analyze_basin) if inspect.isfunction(obj) or inspect.isclass(obj)]
