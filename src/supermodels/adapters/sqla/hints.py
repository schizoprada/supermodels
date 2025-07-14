# ~/supermodels/src/supermodels/adapters/sqla/hints.py
"""
SQLAlchemy Type Hints and Aliases

Type definitions specific to the SQLAlchemy adapter for better type safety
and code readability.
"""
from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
   from sqlalchemy.orm import Session
   from supermodels.core.models.tvars import ModelType

SessionFactory = t.Callable[[], 'Session']

PaginationResult = t.Tuple[t.List['ModelType'], int]
