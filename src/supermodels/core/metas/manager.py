# ~/supermodels/src/supermodels/core/metas/manager.py
"""
Manager Metaclass

Metaclass for automatic model-to-manager registration. When manager classes
are defined, they automatically register which models they handle.
"""
from __future__ import annotations
import abc, typing as t

from supermodels.core.hints import MetaModelRegistry

if t.TYPE_CHECKING:
   from supermodels.core.bases.manager import BaseManager

class ManagerMeta(abc.ABCMeta):
    """Metaclass that automatically registers model-to-manager mappings.

    When a manager class is created with __model__ or __models__ attributes,
    this metaclass automatically registers those models in a global registry.
    This enables dynamic manager lookup at runtime.
    """

    _modelregistry: MetaModelRegistry = {}

    def __new__(cls, name: str, bases: tuple, attrs: dict): #! should add return hint
        """Create new manager class and register its models."""
        newclass = super().__new__(cls, name, bases, attrs)

        skippable = list({'BaseManager'})

        if name in skippable: return newclass

        # register models -> manager mapping if model is defined
        managing = []

        if hasattr(newclass, '__models__') and newclass.__models__: #type: ignore
            managing.extend(newclass.__models__) # type: ignore

        elif hasattr(newclass, '__model__') and newclass.__model__: # type: ignore
            managing.append(newclass.__model__) # type: ignore

        else:
            raise AttributeError(f"Manager class '{name}' must define either '__model__' or '__models__' attribute")

        if not managing:
            raise ValueError(f"Manager class '{name}' has empty model configuration")

        for managed in managing:
            cls._modelregistry[managed] = t.cast(t.Type['BaseManager'], newclass)

        return newclass

    @classmethod
    def GetModelManager(cls, model: t.Type[t.Any]) -> t.Optional[t.Type['BaseManager']]:
        """Get the manager class registered for a model type."""
        return cls._modelregistry.get(model)

    @classmethod
    def GetInstanceMangager(cls, instance: t.Any) -> t.Optional[t.Type['BaseManager']]:
        """Get the manager class registered for an instance's type."""
        return cls._modelregistry.get(type(instance))

    @classmethod
    def GetManager(cls, obj: t.Union[t.Type[t.Any], t.Any]) -> t.Optional[t.Type['BaseManager']]:
        """Get manager for either a model class or instance."""
        if isinstance(obj, type):
            return cls.GetModelManager(obj)
        return cls.GetInstanceMangager(obj)

    @classmethod
    def GetRegistry(cls) -> MetaModelRegistry:
        """Get a copy of the complete model registry."""
        return cls._modelregistry.copy()
