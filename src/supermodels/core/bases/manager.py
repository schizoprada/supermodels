# ~/supermodels/src/supermodels/core/bases/manager.py
"""
Manager Abstract Base Class
"""
from __future__ import annotations
import abc, typing as t

from supermodels.core.models.tvars import SessionType, ModelType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.core.metas.manager import ManagerMeta


class BaseManager(abc.ABC, metaclass=ManagerMeta):
    """..."""
    ...
    __model__: t.Optional[t.Type[t.Any]] = None # set by subclasses for single model
    __models__: t.Tuple[t.Type[t.Any]] = tuple()

    def __init__(self, session: SessionType, adapter: DBAdapter[SessionType]):
        """..."""
        self.session = session
        self.adapter = adapter

    def _getinstancemodel(self, item: t.Any) -> t.Type[t.Any]:
        """..."""
        itype = type(item)
        if (self.__models__ and itype in self.__models__):
            return itype
        elif (self.__model__ and isinstance(item, self.__model__)):
            return self.__model__
        raise ValueError()

    def add(self, item: t.Any) -> t.Any:
        """..."""
        return self.adapter.additem(self.session, item)

    def update(self, item: t.Any) -> t.Any:
        """..."""
        return self.adapter.updateitem(self.session, item)

    def delete(self, item: t.Any) -> bool:
        """..."""
        return self.adapter.deleteitem(self.session, item)

    def get(self, model: t.Optional[t.Type[ModelType]], id: t.Any) -> t.Optional[ModelType]:
        """..."""
        m = model or self.__model__ # convenience for single managed
        if not m:
            raise ValueError()
        return self.adapter.querybyid(self.session, m, id=id)

    def getby(self, model: t.Optional[t.Type[ModelType]], **kwargs: t.Any) -> t.List[ModelType]:
        """..."""
        m = model or self.__model__
        if not m:
            raise ValueError()

        result =  self.adapter.queryby(self.session, m, **kwargs)
        return t.cast(t.List[ModelType], result)
