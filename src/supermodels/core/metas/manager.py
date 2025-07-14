# ~/supermodels/src/supermodels/core/metas/manager.py
"""
Manager Metaclass
"""
from __future__ import annotations
import abc, typing as t

from supermodels.core.hints import MetaModelRegistry

if t.TYPE_CHECKING:
    from supermodels.core.bases.manager import BaseManager

class ManagerMeta(abc.ABCMeta):
    """..."""

    _modelregistry: MetaModelRegistry = {}

    def __new__(cls, name: str, bases: tuple, attrs: dict): #! should add return hint
        """..."""
        newclass = super().__new__(cls, name, bases, attrs)

        # register models -> manager mapping if model is defined
        managing = []

        if hasattr(newclass, '__models__') and newclass.__models__: #type: ignore
            managing.extend(newclass.__models__) # type: ignore

        elif hasattr(newclass, '__model__') and newclass.__model__: # type: ignore
            managing.append(newclass.__model__) # type: ignore

        else:
            raise AttributeError()

        if not managing:
            raise ValueError()

        for managed in managing:
            cls._modelregistry[managed] = t.cast(t.Type['BaseManager'], newclass)

        return newclass

    @classmethod
    def GetModelManager(cls, model: t.Type[t.Any]) -> t.Optional[t.Type['BaseManager']]:
        """..."""
        return cls._modelregistry.get(model)

    @classmethod
    def GetInstanceMangager(cls, instance: t.Any) -> t.Optional[t.Type['BaseManager']]:
        """..."""
        return cls._modelregistry.get(type(instance))

    @classmethod
    def GetManager(cls, obj: t.Union[t.Type[t.Any], t.Any]) -> t.Optional[t.Type['BaseManager']]:
        if isinstance(obj, type):
            return cls.GetModelManager(obj)
        return cls.GetInstanceMangager(obj)

    @classmethod
    def GetRegistry(cls) -> MetaModelRegistry:
        return cls._modelregistry.copy()
