# ~/supermodels/src/supermodels/adapters/__init__.py
"""
Database Adapters

Concrete implementations of database adapters for different frameworks.
Currently supports SQLAlchemy with more adapters planned.
"""

from .sqla import SQLA, SQLAAdapter

__all__ = ['SQLA', 'SQLAAdapter']
