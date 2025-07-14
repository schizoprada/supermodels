# ~/supermodels/src/supermodels/core/bases/__init__.py
"""
Base Classes

Core abstract base classes for managers and adapters. These define the
fundamental interfaces that all concrete implementations must follow.
"""

from .adapter import DBAdapter
from .manager import BaseManager

__all__ = ['DBAdapter', 'BaseManager']
