# ~/supermodels/src/supermodels/core/protos/database.py
"""
Database Related Protocols
"""
from __future__ import annotations
import typing as t

from supermodels.core.models.tvars import SessionProtoType


@t.runtime_checkable
class DBSession(t.Protocol[SessionProtoType]):
    """..."""

    def add(self, instance: t.Any) -> None:
        """..."""
        ...

    def delete(self, instance: t.Any) -> None:
        """..."""
        ...

    def merge(self, instance: t.Any) -> t.Any:
        """..."""
        ...

    def refresh(self, instance: t.Any) -> None:
        """..."""
        ...

    def get(self, model: t.Type[t.Any], id: t.Any) -> t.Optional[t.Any]:
        """..."""
        ...

    def query(self, *args: t.Any) -> t.Any:
        """..."""
        ...

    def commit(self) -> None:
        """..."""
        ...

    def close(self) -> None:
        """..."""
        ...

    def rollback(self) -> None:
        """..."""
        ...


@t.runtime_checkable
class DictableModel(t.Protocol):
    """..."""

    def todict(self, *args: t.Any, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        """..."""
        ...

@t.runtime_checkable
class JsonableModel(t.Protocol):
    """..."""

    def json(self, *args: t.Any, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        """..."""
        ...

SerializableModel = t.Union[
    DictableModel,
    JsonableModel
]
