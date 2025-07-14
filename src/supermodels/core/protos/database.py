# ~/supermodels/src/supermodels/core/protos/database.py
"""
Database Related Protocols

Defines protocol interfaces for database sessions and serializable models.
These protocols ensure compatibility across different database frameworks.
"""
from __future__ import annotations
import typing as t

from supermodels.core.models.tvars import SessionProtoType


@t.runtime_checkable
class DBSession(t.Protocol[SessionProtoType]):
    """Protocol for database session objects.

    Defines the interface that database sessions must implement to work
    with supermodels. Compatible with SQLAlchemy Session, Django ORM, etc.
    """

    def add(self, instance: t.Any) -> None:
        """Add an instance to the session."""
        ...

    def delete(self, instance: t.Any) -> None:
        """Mark an instance for deletion in the session."""
        ...

    def merge(self, instance: t.Any) -> t.Any:
        """Merge an instance into the session."""
        ...

    def refresh(self, instance: t.Any) -> None:
        """Refresh an instance from the database."""
        ...

    def get(self, model: t.Type[t.Any], id: t.Any) -> t.Optional[t.Any]:
        """Get an instance by model class and ID."""
        ...

    def query(self, *args: t.Any) -> t.Any:
        """Create a query object."""
        ...

    def commit(self) -> None:
        """Commit the current transaction."""
        ...

    def close(self) -> None:
        """Close the session."""
        ...

    def rollback(self) -> None:
        """Rollback the current transaction."""
        ...


@t.runtime_checkable
class DictableModel(t.Protocol):
    """Protocol for models that can be converted to dictionaries."""

    def todict(self, *args: t.Any, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        """Convert model instance to dictionary representation."""
        ...

@t.runtime_checkable
class JsonableModel(t.Protocol):
    """Protocol for models that can be converted to JSON-compatible format."""

    def json(self, *args: t.Any, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        """Convert model instance to JSON-compatible dictionary."""
        ...

SerializableModel = t.Union[
   DictableModel,
   JsonableModel
]
