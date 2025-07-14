# ~/supermodels/src/supermodels/core/bases/manager.py
"""
Manager Abstract Base Class

Base class for all database model managers. Provides standard CRUD operations
and automatic model registration through the ManagerMeta metaclass.
"""
from __future__ import annotations
import abc, typing as t

from supermodels.core.models.tvars import SessionType, ModelType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.core.metas.manager import ManagerMeta


class BaseManager(abc.ABC, metaclass=ManagerMeta):
    """Abstract base class for model managers.

    Managers handle CRUD operations for specific database models. They use
    database adapters to provide a consistent interface across different
    database frameworks.

    Attributes:
        __model__: Single model class this manager handles
        __models__: Multiple model classes this manager handles
    """
    __model__: t.Optional[t.Type[t.Any]] = None # set by subclasses for single model
    __models__: t.Tuple[t.Type[t.Any], ...] = tuple()

    def __init__(self, session: SessionType, adapter: DBAdapter[SessionType]):
        """Initialize manager with session and adapter."""
        self.session = session
        self.adapter = adapter

    def _getinstancemodel(self, item: t.Any) -> t.Type[t.Any]:
        """Get the model class for a given instance."""
        itype = type(item)
        if (self.__models__ and itype in self.__models__):
            return itype
        elif (self.__model__ and isinstance(item, self.__model__)):
            return self.__model__
        raise ValueError(
            f"""No model found for instance type '{itype.__name__}'.
            Available models: {
                [
                    m.__name__ if hasattr(m, '__name__') else str(m)
                    for m in (self.__models__ or [self.__model__] if self.__model__ else [])
                ]
            }
            """
        )

    def add(self, item: t.Any) -> t.Any:
        """Add an item to the database."""
        return self.adapter.additem(self.session, item)

    def update(self, item: t.Any) -> t.Any:
        """Update an existing item in the database."""
        return self.adapter.updateitem(self.session, item)

    def delete(self, item: t.Any) -> bool:
        """Delete an item from the database."""
        return self.adapter.deleteitem(self.session, item)

    def get(self, model: t.Optional[t.Type[ModelType]], id: t.Any) -> t.Optional[ModelType]:
        """Get an item by ID, optionally specifying model type."""
        m = model or self.__model__ # convenience for single managed
        if not m:
            raise ValueError("No model provided and no default model configured for this manager")
        return self.adapter.querybyid(self.session, m, id=id)

    def getby(self, model: t.Optional[t.Type[ModelType]], **kwargs: t.Any) -> t.List[ModelType]:
        """Get items by filter criteria, optionally specifying model type."""
        m = model or self.__model__
        if not m:
            raise ValueError("No model provided and no default model configured for this manager")

        result =  self.adapter.queryby(self.session, m, **kwargs)
        return t.cast(t.List[ModelType], result)
