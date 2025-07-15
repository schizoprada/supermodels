# ~/supermodels/src/supermodels/core/manager.py
"""
Concrete Manager Implementation

Main Manager class and ManagerContext for database operations with dynamic
method dispatch and model registration. Provides the primary user interface
for context-managed database operations.
"""
from __future__ import annotations
import typing as t

from supermodels.core.models.tvars import SessionType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.core.metas.manager import ManagerMeta
from supermodels.core.models.contexts import ManagerContext

if t.TYPE_CHECKING:
   from sqlalchemy.engine import Engine as SQLAEngine


class Manager:
    """Main manager factory for creating database operation contexts.

    Provides factory methods for different database adapters and supports
    global default adapter configuration via __getitem__.
    """
    _defaultadapter: t.Optional[DBAdapter] = None

    def __init__(self, adapter: t.Optional[DBAdapter[SessionType]] = None, *models: t.Type[t.Any]) -> None:
        """Initialize manager with adapter or use global default."""
        _adapter = (adapter or self._defaultadapter)
        if not _adapter:
            raise ValueError("No adapter provided and no default adapter configured")
        self.adapter: DBAdapter = _adapter
        self.models = models
        self._context: t.Optional[ManagerContext] = None

    def __enter__(self) -> 'ManagerContext':
        """Enter context manager mode using models provided during init."""
        if not self.models:
            raise ValueError("At least one model must be provided")
        if (len(self.models) != len(set(self.models))):
            raise ValueError("Duplicate models provided")
        self._context = self(*self.models)
        return self._context.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager mode."""
        if self._context:
            result = self._context.__exit__(exc_type, exc_val, exc_tb)
            self._context = None
            return result

    def __call__(self, *models: t.Type[t.Any]) -> 'ManagerContext':
        """Create a ManagerContext for the specified models."""
        if not models:
            raise ValueError("At least one model must be provided")
        if (len(models) != len(set(models))):
            raise ValueError("Duplicate models provided")

        unregistered = [
            model for model in models
            if not ManagerMeta.GetModelManager(model)
        ]

        if unregistered:
            raise ValueError(f"No managers registered for models: {[m.__name__ for m in unregistered]}")

        return ManagerContext(self.adapter, *models)

    @classmethod
    def __getitem__(cls, adapter: DBAdapter) -> t.Type['Manager']:
        """Set global default adapter for convenience."""
        cls._defaultadapter = adapter
        return cls

    @classmethod
    def SQLA(cls, engine: 'SQLAEngine') -> 'Manager':
        """Factory method for SQLAlchemy adapter."""
        from supermodels.adapters.sqla import SQLAAdapter
        adapter = SQLAAdapter(engine)
        return cls(adapter)
