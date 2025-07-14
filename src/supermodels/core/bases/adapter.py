# ~/supermodels/src/supermodels/core/bases/adapter.py
"""
Database Adapter Base
"""
from __future__ import annotations
import abc, typing as t

from supermodels.core.models.tvars import ModelType, SessionType


class DBAdapter(abc.ABC, t.Generic[SessionType]):
    """..."""

    @abc.abstractmethod
    def createsession(self) -> SessionType:
        """..."""
        pass

    @abc.abstractmethod
    def closesession(self, session: SessionType) -> None:
        """..."""
        pass

    @abc.abstractmethod
    def queryall(self, session: SessionType, model: t.Type[ModelType]) -> t.List[ModelType]:
        """..."""
        pass

    @abc.abstractmethod
    def queryby(self, session: SessionType, model: t.Type[ModelType], **filters: t.Any) -> t.List[ModelType]:
        """..."""
        pass

    @abc.abstractmethod
    def queryoneby(self, session: SessionType, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        """..."""
        pass

    @abc.abstractmethod
    def querybyid(self, session: SessionType, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        """..."""
        pass

    @abc.abstractmethod
    def additem(self, session: SessionType, item: t.Any) -> t.Any:
        """..."""
        pass

    @abc.abstractmethod
    def updateitem(self, session: SessionType, item: t.Any) -> t.Any:
        """..."""
        pass

    @abc.abstractmethod
    def deleteitem(self, session: SessionType, item: t.Any) -> bool:
        """..."""
        pass
