# ~/supermodels/src/supermodels/__init__.py
"""
supermodels
-----------

Type-safe, framework-agnostic database managers with context management.
Provides a unified interface for database operations across different ORMs
with automatic model registration and dynamic method dispatch.

Features:
- Context-managed database operations
- Dynamic method dispatch based on object types
- Automatic model-to-manager registration
- Support for custom model operations
- SQLAlchemy adapter with pagination and bulk operations
- Type-safe interfaces with full IDE support

Example:
    >>> from supermodels import Manager
    >>> from supermodels.adapters import SQLA
    >>> from sqlalchemy import create_engine
    >>>
    >>> engine = create_engine('sqlite:///example.db')
    >>> manager = Manager(SQLA(engine))
    >>>
    >>> with manager(User, Order) as mgr:
    ...     user = mgr.add(User(name="John"))
    ...     order = mgr.add(Order(user_id=user.id))
"""

__version__ = "0.1.18"
__author__ = "Joel Yisrael"
__email__ = "schizoprada@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/schizoprada/supermodels"

VERSION = tuple(map(int, __version__.split('.')))

from .core.manager import Manager, ManagerContext
from .core.bases import BaseManager, DBAdapter
from .core.metas import ManagerMeta

__all__ = [
    'Manager',
    'ManagerContext',
    'BaseManager',
    'DBAdapter',
    'ManagerMeta',
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__url__',
    'VERSION'
]
