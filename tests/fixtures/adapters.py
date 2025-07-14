# ~/supermodels/tests/fixtures/adapters.py
from typing import Type, Optional, List, Any
from supermodels.core.bases.adapter import DBAdapter

class MockSession:
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True

class MockAdapter(DBAdapter[MockSession]):
    def __init__(self):
        self.sessions = []
        self.added_items = []
        self.updated_items = []
        self.deleted_items = []

    def createsession(self) -> MockSession:
        session = MockSession()
        self.sessions.append(session)
        return session

    def closesession(self, session: MockSession) -> None:
        session.close()

    def queryall(self, session: MockSession, model: Type[Any]) -> List[Any]:
        return [model(id=1), model(id=2)]

    def queryby(self, session: MockSession, model: Type[Any], **kwargs) -> List[Any]:
        return [model(id=kwargs.get('id', 1))]

    def queryoneby(self, session: MockSession, model: Type[Any], **kwargs) -> Optional[Any]:
        return model(id=kwargs.get('id', 1))

    def querybyid(self, session: MockSession, model: Type[Any], **kwargs) -> Optional[Any]:
        return model(id=kwargs.get('id', 1))

    def additem(self, session: MockSession, item: Any) -> Any:
        self.added_items.append(item)
        session.commit()
        return item

    def updateitem(self, session: MockSession, item: Any) -> Any:
        self.updated_items.append(item)
        session.commit()
        return item

    def deleteitem(self, session: MockSession, item: Any) -> bool:
        self.deleted_items.append(item)
        session.commit()
        return True
