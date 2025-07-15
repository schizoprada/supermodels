# ~/supermodels/src/supermodels/core/utils/decorators.py
"""
Decorators

Utility decorators for enhancing class functionality. Includes decorators
for automatic operation registration and method dispatch in manager contexts.
"""
from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from supermodels.core.bases.manager import BaseManager
    from supermodels.core.models.contexts import ManagerContext


agnosticops = {'add', 'update', 'delete'}
defaultops = agnosticops | {'get', 'getby'}

def createopmethod(opname: str) -> t.Callable:
    """Create a bound method for an operation."""
    def opmethod(self, *args, **kwargs):
        return self._dispatch(opname, *args, **kwargs)
    opmethod.__name__ = opname
    return opmethod


def _registerforctx(cls) -> t.Type['ManagerContext']:
    """Decorator to register CRUD and custom operations on ManagerContext.

    Automatically adds default CRUD operations (add, update, delete, get, getby)
    and any custom operations defined in model __super__ attributes.
    """
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

def _registerforbase(cls) -> t.Type['BaseManager']:
    """Decorator to register CRUD and custom operations on BaseManager.

    Adds default CRUD operations and custom operations defined in model
    __super__ attributes directly to the manager class at class creation time.
    """

    def dispatch(self, opname: str, *args, **kwargs) -> t.Any:
        """Route operations to manager methods or model class methods."""
        if not args:
            raise ValueError(f"Operation '{opname}' requires at least one argument")

        # Route default CRUD operations to existing manager methods
        if opname in defaultops:
            try:
                return getattr(self, opname)(*args, **kwargs)
            except Exception as e:
                raise ValueError(f"Cannot perform '{opname}': {e}")

        # Determine which models to check for custom operations
        checkable = self.__models__ if self.__models__ else [self.__model__]
        if (not checkable) or any(m is None for m in checkable):
            raise ValueError("No models configured for this manager")

        # Search for custom operation in managed models
        for model in checkable:
            if hasattr(model, opname):
                try:
                    method = getattr(model, opname)
                    return method(self.session, *args, **kwargs)
                except Exception as e:
                    raise RuntimeError(f"Error executing custom operation '{opname}': {e}")

        raise AttributeError(f"Operation '{opname}' not found in managed models")

    def customize():
        """Add operation methods to the class based on managed models."""
        # Collect custom operations from class-level model definitions
        customops = set()
        if hasattr(cls, '__models__') and cls.__models__:
            for model in cls.__models__:
                if hasattr(model, '__super__') and model.__super__:
                    customops.update(model.__super__)
        elif hasattr(cls, '__model__') and cls.__model__:
            if hasattr(cls.__model__, '__super__') and cls.__model__.__super__:
                customops.update(cls.__model__.__super__)

        # Add all operations (default + custom) to class if not already present
        for opname in (defaultops | customops):
            if not hasattr(cls, opname):
                setattr(cls, opname, createopmethod(opname))

    cls._dispatch = dispatch
    customize()
    return cls


@t.overload
def registeroperations(cls: t.Type['ManagerContext']) -> t.Type['ManagerContext']: ...

@t.overload
def registeroperations(cls: t.Type['BaseManager']) -> t.Type['BaseManager']: ...

def registeroperations(cls: t.Type):
    """
    Register CRUD and custom operations on manager classes.

    Automatically adds default CRUD operations and any custom operations
    defined in model __super__ attributes. Behavior varies by class type:
    - ManagerContext: Operations route through manager registry
    - BaseManager: Operations route directly to class methods or models
    """
    from supermodels.core.bases.manager import BaseManager
    from supermodels.core.models.contexts import ManagerContext

    if issubclass(cls, ManagerContext):
        return _registerforctx(cls)
    elif issubclass(cls, BaseManager):
        return _registerforbase(cls)
    else:
        raise TypeError(f"registeroperations can only be applied to BaseManager or ManagerContext subclasses, got {cls}")
