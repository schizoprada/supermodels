# ~/supermodels/src/supermodels/adapters/sqla/adapter.py
"""
SQLAlchemy Database Adapter
"""
from __future__ import annotations
import typing as t

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine

from supermodels.core.models.tvars import ModelType
from supermodels.core.bases.adapter import DBAdapter
from supermodels.adapters.sqla.hints import SessionFactory, PaginationResult
from supermodels.adapters.sqla.enums import OrderBy, ASC, DESC

class SQLAAdapter(DBAdapter[Session]):
    """..."""

    def __init__(
        self,
        engine: Engine,
        sessionfactory: t.Optional[SessionFactory] = None,
    ) -> None:
        """..."""
        self.engine = engine
        self.sessionfactory = (sessionfactory or sessionmaker(bind=engine))


    def createsession(self) -> Session:
        return self.sessionfactory()

    def closesession(self, session: Session) -> None:
        session.close()

    def queryall(self, session: Session, model: t.Type[ModelType]) -> t.List[ModelType]:
        return session.query(model).all()

    def queryby(self, session: Session, model: t.Type[ModelType], **filters: t.Any) -> t.List[ModelType]:
        query = session.query(model)

        for k,v in filters.items():
            if hasattr(model, k):
                query = query.filter(getattr(model, k) == v)

        return query.all()

    def queryoneby(self, session: Session, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        results = self.queryby(session, model, **kwargs)
        if results:
            return results[0]
        return None

    def querybyid(self, session: Session, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        idval = kwargs.get('id')
        if idval is None: return None
        return session.query(model).get(idval)

    def additem(self, session: Session, item: t.Any) -> t.Any:
        session.add(item)
        session.commit()
        return item

    def updateitem(self, session: Session, item: t.Any) -> t.Any:
        merged = session.merge(item)
        session.commit()
        session.refresh(merged)
        return merged

    def deleteitem(self, session: Session, item: t.Any) -> bool:
        try:
            session.delete(item)
            session.commit()
            return True
        except Exception as e:
            import warnings
            session.rollback()
            warnings.warn(f"Error deleting item: {item!r}\nError: {e}")
            return False

    def querypage(
        self,
        session: Session,
        model: t.Type[ModelType],
        page: int = 1,
        hits: int = 25,
        sortby: str = 'id',
        orderby: OrderBy = DESC,
        **filters: t.Any
    ) -> PaginationResult:
        """..."""
        query = session.query(model)

        for k,v in filters.items():
            if hasattr(model, k):
                query = query.filter(getattr(model, k) == v)

        total = query.count()

        if hasattr(model, sortby):
            query = query.order_by(orderby.func(getattr(model, sortby)))
        offset = ((page - 1) * hits)

        items = query.offset(offset).limit(hits).all()

        return (items, total)

    def bulkadd(self, session: Session, *items: t.Any) -> t.List[t.Any]:
        """..."""
        session.add_all(list(items))
        session.commit()
        return list(items)

    def bulkupdate(self, session: Session, *items: t.Any) -> t.List[t.Any]:
        for item in items:
            session.merge(item)
        session.commit()
        return list(items)

    def bulkdelete(self, session: Session, *items: t.Any) -> bool:
        """..."""
        try:
            for item in items: session.delete(item)
            session.commit()
            return True
        except Exception as e:
            import warnings
            session.rollback()
            warnings.warn(f"Error bulk deleting: {e}")
            return False


"""
- bulkdelete // should probably add way to track individual failures, variate return type // keep it simple for now tho
    if `deletion` wasnt unbound this would be so sexy:
                if (failures:=[
                    (deletion:=session.delete(item))
                    for item in items if not deletion
                ])

"""
