# ~/supermodels/src/supermodels/core/manager.py
"""
Concrete Manager
"""
from __future__ import annotations
import typing as t

from supermodels.core.hints import ManagerInstanceRegistry
from supermodels.core.models.tvars import SessionType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.core.bases.manager import BaseManager
from supermodels.core.metas.manager import ManagerMeta


def registeroperations(cls):
    """..."""
    agnosticops = {'add', 'update', 'delete'}
    defaultops = agnosticops | {'get', 'getby'}

    def dispatch(self, opname: str, *args, **kwargs) -> t.Any:
        """..."""
        if not args: raise ValueError()

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
                if not isinstance(model, type): raise ValueError()
                if (model not in self._managersregistry): raise ValueError()

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
                    raise RuntimeError(f"Error executing '{opname}': {e}")

        raise AttributeError(f"({opname}) operation not found")

    def createopmethod(opname: str) -> t.Callable:
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
    """..."""
    def __init__(self, adapter: DBAdapter[SessionType], *models: t.Type[t.Any]) -> None:
        """..."""
        self.adapter = adapter
        self.models = models
        self.session: t.Optional[SessionType] = None
        self._managersregistry: ManagerInstanceRegistry = {}

    def __enter__(self) -> 'ManagerContext[SessionType]':
        """..."""
        self.session = self.adapter.createsession()

        for model in self.models:
            managerclass = ManagerMeta.GetModelManager(model)
            if managerclass:
                self._managersregistry[model] = managerclass(self.session, self.adapter)


        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """..."""
        if self.session:
            if exc_type:
                self.session.rollback() # type: ignore
            self.adapter.closesession(self.session)

    def _getmanager(self, item: t.Any) -> BaseManager:
        """..."""
        if item is None: raise ValueError()

        itype = type(item)

        if (itype in self._managersregistry):
            return self._managersregistry[itype]

        for model, manager in self._managersregistry.items():
            if isinstance(item, model):
                return manager

        raise ValueError()

class Manager:
    """..."""

    def __init__(self, adapter: DBAdapter[SessionType]):
        """..."""
        self.adapter = adapter

    def __call__(self, *models: t.Type[t.Any]) -> 'ManagerContext':
        """..."""
        if not models: raise ValueError()
        if (len(models) != len(set(models))): raise ValueError()


        unregistered = [
            model for model in models
            if not ManagerMeta.GetModelManager(model)
        ]

        if unregistered: raise ValueError()

        return ManagerContext(self.adapter, *models)
