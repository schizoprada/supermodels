# ~/supermodels/src/supermodels/adapters/sqla/adapter.py
"""
SQLAlchemy Database Adapter

Concrete implementation of DBAdapter for SQLAlchemy ORM. Provides full
database operations including advanced features like pagination and bulk operations.
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
    """SQLAlchemy implementation of the database adapter interface.

    Provides full CRUD operations, pagination, bulk operations, and advanced
    querying capabilities using SQLAlchemy ORM.
    """

    def __init__(
        self,
        engine: Engine,
        sessionfactory: t.Optional[SessionFactory] = None,
    ) -> None:
        """Initialize adapter with SQLAlchemy engine and optional session factory."""
        self.engine = engine
        self.sessionfactory = (sessionfactory or sessionmaker(bind=engine))

    def createsession(self) -> Session:
        """Create a new SQLAlchemy session."""
        return self.sessionfactory()

    def closesession(self, session: Session) -> None:
        """Close a SQLAlchemy session."""
        session.close()

    def queryall(self, session: Session, model: t.Type[ModelType]) -> t.List[ModelType]:
        """Query all records of a model type."""
        return session.query(model).all()

    def queryby(self, session: Session, model: t.Type[ModelType], **filters: t.Any) -> t.List[ModelType]:
        """Query records with filter criteria."""
        query = session.query(model)

        for k,v in filters.items():
            if hasattr(model, k):
                query = query.filter(getattr(model, k) == v)

        return query.all()

    def queryoneby(self, session: Session, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        """Query a single record with filter criteria."""
        results = self.queryby(session, model, **kwargs)
        if results:
            return results[0]
        return None

    def querybyid(self, session: Session, model: t.Type[ModelType], **kwargs: t.Any) -> t.Optional[ModelType]:
        """Query a record by its ID."""
        idval = kwargs.get('id')
        if idval is None: return None
        return session.query(model).get(idval)

    def additem(self, session: Session, item: t.Any) -> t.Any:
        """Add an item to the database."""
        session.add(item)
        session.commit()
        return item

    def updateitem(self, session: Session, item: t.Any) -> t.Any:
        """Update an existing item in the database."""
        merged = session.merge(item)
        session.commit()
        session.refresh(merged)
        return merged

    def deleteitem(self, session: Session, item: t.Any) -> bool:
        """Delete an item from the database."""
        try:
            session.delete(item)
            session.commit()
            return True
        except Exception as e:
            import warnings
            session.rollback()
            warnings.warn(f"Failed to delete item {item!r}: {e}")
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
        """Query records with pagination and sorting."""
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
        """Add multiple items to the database in a single transaction."""
        session.add_all(list(items))
        session.commit()
        return list(items)

    def bulkupdate(self, session: Session, *items: t.Any) -> t.List[t.Any]:
        """Update multiple items in the database in a single transaction."""
        for item in items:
            session.merge(item)
        session.commit()
        return list(items)

    def bulkdelete(self, session: Session, *items: t.Any) -> bool:
        """Delete multiple items from the database in a single transaction."""
        try:
            for item in items: session.delete(item)
            session.commit()
            return True
        except Exception as e:
            import warnings
            session.rollback()
            warnings.warn(f"Failed to bulk delete items: {e}")
            return False


"""
- bulkdelete // should probably add way to track individual failures, variate return type // keep it simple for now tho
    if `deletion` wasnt unbound this would be so sexy:
                if (failures:=[
                    (deletion:=session.delete(item))
                    for item in items if not deletion
                ])

"""
