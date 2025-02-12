"""
This module initializes the SARDS package.
"""

from . import core  # Import the module itself
from . import ast_nodes
from . import data_types
from . import user_functions

from .core import * # Import core components
from .ast_nodes import * # Import AST Nodes
from .data_types import * # Import Data Types
from .user_functions import * # Import User Function

# Define what is exposed when doing `from mypackage import *`
__all__ = [
    *core.__all__,
    *ast_nodes.__all__,
    *data_types.__all__,
    *user_functions.__all__
]
