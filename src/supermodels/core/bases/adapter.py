# ~/supermodels/src/supermodels/core/bases/adapter.py
"""
Database Adapter Abstract Base

Abstract interface for database operations. Adapters provide a consistent
API across different database frameworks (SQLAlchemy, Django ORM, etc.).
"""
from __future__ import annotations
import abc, typing as t

from supermodels.core.models.tvars import ModelType, SessionType


class DBAdapter(abc.ABC, t.Generic[SessionType]):
    """Abstract base class for database adapters.

    Database adapters translate between the supermodels API and specific
    database frameworks. Each adapter implements this interface to provide
    consistent database operations.
    """

    @abc.abstractmethod
    def createsession(self) -> SessionType:
        """Create a new database session."""
        pass

    @abc.abstractmethod
    def closesession(self, session: SessionType) -> None:
        """Close a database session."""
        pass

    @abc.abstractmethod
    def queryall(self, session: SessionType, model: t.Type[ModelType]) -> t.List[ModelType]:
        """Query all records of a model type."""
        pass

    @abc.abstractmethod
    def queryby(self, session: SessionType, model: t.Type[ModelType], **filters: t.Any) -> t.List[ModelType]:
        """Query records with filter criteria."""
        pass

    @abc.abstractmethod
    def queryoneby(self, session: SessionType, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        """Query a single record with filter criteria."""
        pass

    @abc.abstractmethod
    def querybyid(self, session: SessionType, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        """Query a record by its ID."""
        pass

    @abc.abstractmethod
    def additem(self, session: SessionType, item: t.Any) -> t.Any:
        """Add an item to the database."""
        pass

    @abc.abstractmethod
    def updateitem(self, session: SessionType, item: t.Any) -> t.Any:
        """Update an item in the database."""
        pass

    @abc.abstractmethod
    def deleteitem(self, session: SessionType, item: t.Any) -> bool:
        """Delete an item from the database."""
        pass
