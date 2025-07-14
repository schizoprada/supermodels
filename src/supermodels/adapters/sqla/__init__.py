# ~/supermodels/src/supermodels/adapters/sqla/__init__.py
"""
SQLAlchemy Adapter

Complete SQLAlchemy implementation with advanced features like pagination,
bulk operations, and optimized querying.
"""

from .adapter import SQLAAdapter
from .enums import OrderBy, ASC, DESC
from .hints import SessionFactory, PaginationResult

SQLA = SQLAAdapter

__all__ = ['SQLAAdapter', 'SQLA', 'OrderBy', 'ASC', 'DESC', 'SessionFactory', 'PaginationResult']
