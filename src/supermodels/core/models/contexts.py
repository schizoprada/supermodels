# ~/supermodels/src/supermodels/core/models/contexts.py
"""
Manager Contexts

Context manager implementations for database operations with dynamic method
dispatch. Provides context-managed interfaces that automatically route
operations to appropriate managers based on object types.
"""
from __future__ import annotations
import typing as t

from supermodels.core.hints import ManagerInstanceRegistry
from supermodels.core.models.tvars import SessionType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.core.bases.manager import BaseManager
from supermodels.core.metas.manager import ManagerMeta
from supermodels.core.utils.decorators import registeroperations


@registeroperations
class ManagerContext(t.Generic[SessionType]):
    """Context manager for database operations with dynamic method dispatch.

    Provides a context-managed interface for database operations that automatically
    routes method calls to appropriate managers based on object types. Supports
    both default CRUD operations and custom model-specific operations.
    """
    def __init__(self, adapter: DBAdapter[SessionType], *models: t.Type[t.Any]) -> None:
        """Initialize context with adapter and models to manage."""
        self.adapter = adapter
        self.models = models
        self.session: t.Optional[SessionType] = None
        self._managersregistry: ManagerInstanceRegistry = {}

    def __enter__(self) -> t.Self:
        """Enter context and create session with manager instances."""
        self.session = self.adapter.createsession()

        for model in self.models:
            managerclass = ManagerMeta.GetModelManager(model)
            if managerclass:
                self._managersregistry[model] = managerclass(self.session, self.adapter)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context and clean up session."""
        if self.session:
            if exc_type:
                self.session.rollback() # type: ignore
            self.adapter.closesession(self.session)

    def _getmanager(self, item: t.Any) -> BaseManager:
        """Get the appropriate manager for an item instance."""
        if item is None:
            raise ValueError("Cannot get manager for None item")

        itype = type(item)

        if (itype in self._managersregistry):
            return self._managersregistry[itype]

        for model, manager in self._managersregistry.items():
            if isinstance(item, model):
                return manager

        raise ValueError(f"No manager found for type '{itype.__name__}'. Available types: {[t.__name__ for t in self._managersregistry.keys()]}")
