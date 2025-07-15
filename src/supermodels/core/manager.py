# ~/supermodels/src/supermodels/core/manager.py
"""
Concrete Manager Implementation

Main Manager class and ManagerContext for database operations with dynamic
method dispatch and model registration. Provides the primary user interface
for context-managed database operations.
"""
from __future__ import annotations
import typing as t

from supermodels.core.hints import ManagerInstanceRegistry
from supermodels.core.models.tvars import SessionType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.core.bases.manager import BaseManager
from supermodels.core.metas.manager import ManagerMeta

if t.TYPE_CHECKING:
   from sqlalchemy.orm import Session as SQLASession
   from sqlalchemy.engine import Engine as SQLAEngine

def registeroperations(cls):
    """Decorator to register CRUD and custom operations on ManagerContext.

    Automatically adds default CRUD operations (add, update, delete, get, getby)
    and any custom operations defined in model __super__ attributes.
    """
    agnosticops = {'add', 'update', 'delete'}
    defaultops = agnosticops | {'get', 'getby'}

    def dispatch(self, opname: str, *args, **kwargs) -> t.Any:
        """Route operations to appropriate managers or model methods."""
        if not args:
            raise ValueError(f"Operation '{opname}' requires at least one argument")

        if (opname in defaultops):
            if opname in agnosticops:
                try:
                    manager = self._getmanager(args[0])
                    return getattr(manager, opname)(*args, **kwargs)
                except Exception as e:
                    raise ValueError(f"Cannot perform '{opname}': {e}")
            else:
                # handle get/getby
                model = args[0]
                if not isinstance(model, type):
                    raise ValueError(f"Operation '{opname}' requires model class as first argument, got {type(model).__name__}")
                if (model not in self._managersregistry):
                    raise ValueError(f"No manager registered for model '{model.__name__}'")

                try:
                    manager = self._managersregistry[model]
                    return getattr(manager, opname)(*args, **kwargs)
                except Exception as e:
                    raise ValueError(f"Cannot perform '{opname}': {e}")

        for model in self.models:
            if hasattr(model, opname):
                try:
                    method = getattr(model, opname)
                    return method(self.session, *args, **kwargs)
                except Exception as e:
                    raise RuntimeError(f"Error executing custom operation '{opname}': {e}")

        raise AttributeError(f"Operation '{opname}' not found in any registered models")

    def createopmethod(opname: str) -> t.Callable:
        """Create a bound method for an operation."""
        def opmethod(self, *args, **kwargs):
            return self._dispatch(opname, *args, **kwargs)
        opmethod.__name__ = opname
        return opmethod

    oginit = cls.__init__

    def initialize(self, adapter, *models):
        import types

        oginit(self, adapter, *models)

        customops = set()
        for model in models:
            if hasattr(model, '__super__') and model.__super__:
                customops.update(model.__super__)

        for opname in (defaultops | customops):
            if not hasattr(self, opname):
                method = createopmethod(opname)
                bound = types.MethodType(method, self) # bind to instance
                setattr(self, opname, bound)

    cls._dispatch = dispatch
    cls.__init__ = initialize

    return cls

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

    def __enter__(self) -> 'ManagerContext[SessionType]':
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

class Manager:
    """Main manager factory for creating database operation contexts.

    Provides factory methods for different database adapters and supports
    global default adapter configuration via __getitem__.
    """
    _defaultadapter: t.Optional[DBAdapter] = None

    def __init__(self, adapter: t.Optional[DBAdapter[SessionType]] = None):
        """Initialize manager with adapter or use global default."""
        _adapter = (adapter or self._defaultadapter)
        if not _adapter:
            raise ValueError("No adapter provided and no default adapter configured")
        self.adapter: DBAdapter = _adapter

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
            unregistered_names = [m.__name__ for m in unregistered]
            raise ValueError(f"No managers registered for models: {unregistered_names}")

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
