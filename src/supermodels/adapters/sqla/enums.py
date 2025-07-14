# ~/supermodels/src/supermodels/adapters/sqla/enums.py
"""
...
"""
from __future__ import annotations
import enum, typing as t

class OrderBy(str, enum.Enum):
    ASC = "asc"
    DESC = "desc"

    @property
    def func(self) -> t.Callable:
        from sqlalchemy import asc, desc
        match self.value:
            case "asc":
                return asc
            case "desc":
                return desc
            case _:
                # unreachable
                raise ValueError()

ASC = OrderBy.ASC
DESC = OrderBy.DESC
