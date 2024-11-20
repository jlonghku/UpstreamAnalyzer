# __init__.py

__version__ = '0.1.4'
__author__ = 'Long Jiang'

import inspect
import sys

# Dynamically import all functions and classes from analyze_basin.py
from . import analyze_basin

# Add all functions and classes from analyze_basin to the module's namespace dynamically
for name, obj in inspect.getmembers(analyze_basin):
    if inspect.isfunction(obj) or inspect.isclass(obj):
        setattr(sys.modules[__name__], name, obj)

# Update the __all__ list dynamically
__all__ = [name for name, obj in inspect.getmembers(analyze_basin) if inspect.isfunction(obj) or inspect.isclass(obj)]
