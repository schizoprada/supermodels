# ~/supermodels/src/supermodels/adapters/sqla/enums.py
"""
SQLAlchemy Enumerations

Enums for SQLAlchemy adapter configuration and operations.
"""
from __future__ import annotations
import enum, typing as t

class OrderBy(str, enum.Enum):
    """Enumeration for query ordering directions."""
    ASC = "asc"
    DESC = "desc"

    @property
    def func(self) -> t.Callable:
        """Get the corresponding SQLAlchemy ordering function."""
        from sqlalchemy import asc, desc
        match self.value:
            case "asc":
                return asc
            case "desc":
                return desc
            case _:
                # unreachable
                raise ValueError(f"Invalid OrderBy value: {self.value}")

ASC = OrderBy.ASC
DESC = OrderBy.DESC
