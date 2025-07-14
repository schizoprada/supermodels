# ~/supermodels/tests/unit/core/bases/test_adapter.py
import pytest
from abc import ABC
from supermodels.core.bases.adapter import DBAdapter
from tests.fixtures.models import User, Order

class TestDBAdapter:

   def test_is_abstract_class(self):
       """Test DBAdapter is abstract and cannot be instantiated"""
       with pytest.raises(TypeError):
           DBAdapter()

   def test_concrete_implementation_works(self):
       """Test concrete implementation can be instantiated"""
       class ConcreteAdapter(DBAdapter):
           def createsession(self):
               return "mock_session"

           def closesession(self, session):
               pass

           def queryall(self, session, model):
               return []

           def queryby(self, session, model, **filters):
               return []

           def queryoneby(self, session, model, **kwargs):
               return None

           def querybyid(self, session, model, **kwargs):
               return None

           def additem(self, session, item):
               return item

           def updateitem(self, session, item):
               return item

           def deleteitem(self, session, item):
               return True

       adapter = ConcreteAdapter()
       assert adapter is not None

   def test_missing_methods_raises_error(self):
       """Test implementation missing abstract methods raises error"""
       with pytest.raises(TypeError):
           class IncompleteAdapter(DBAdapter):
               def createsession(self):
                   return "session"
               # Missing other required methods

           IncompleteAdapter()

   def test_all_abstract_methods_defined(self):
       """Test all expected abstract methods are defined"""
       expected_methods = {
           'createsession',
           'closesession',
           'queryall',
           'queryby',
           'queryoneby',
           'querybyid',
           'additem',
           'updateitem',
           'deleteitem'
       }

       actual_methods = {
           name for name, method in DBAdapter.__dict__.items()
           if hasattr(method, '__isabstractmethod__') and method.__isabstractmethod__
       }

       assert actual_methods == expected_methods

   def test_generic_typing(self):
       """Test adapter supports generic typing"""
       class MockSession:
           pass

       class TypedAdapter(DBAdapter[MockSession]):
           def createsession(self) -> MockSession:
               return MockSession()

           def closesession(self, session: MockSession) -> None:
               pass

           def queryall(self, session: MockSession, model):
               return []

           def queryby(self, session: MockSession, model, **filters):
               return []

           def queryoneby(self, session: MockSession, model, **kwargs):
               return None

           def querybyid(self, session: MockSession, model, **kwargs):
               return None

           def additem(self, session: MockSession, item):
               return item

           def updateitem(self, session: MockSession, item):
               return item

           def deleteitem(self, session: MockSession, item):
               return True

       adapter = TypedAdapter()
       session = adapter.createsession()
       assert isinstance(session, MockSession)
