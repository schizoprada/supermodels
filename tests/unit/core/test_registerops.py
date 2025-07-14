# ~/supermodels/tests/unit/core/test_registerops.py
# tests/unit/core/test_registerops.py
import pytest
from supermodels.core.manager import registeroperations, ManagerContext
from supermodels.core.bases.manager import BaseManager
from tests.fixtures.models import User, Order
from tests.fixtures.adapters import MockAdapter

class TestRegisterOperations:

   def test_decorator_adds_default_operations(self, mock_adapter):
       """Test decorator adds default CRUD operations"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       # Check default operations exist
       assert hasattr(context, 'add')
       assert hasattr(context, 'update')
       assert hasattr(context, 'delete')
       assert hasattr(context, 'get')
       assert hasattr(context, 'getby')

   def test_decorator_adds_custom_operations(self, mock_adapter):
       """Test decorator adds custom operations from models"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)  # User has __super__ = {'GetOrders', 'GetAddresses'}

       # Check custom operations exist
       assert hasattr(context, 'GetOrders')
       assert hasattr(context, 'GetAddresses')

   def test_decorator_preserves_original_init(self, mock_adapter):
       """Test decorator preserves original __init__ behavior"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User, Order)

       # Original init behavior should work
       assert context.adapter == mock_adapter
       assert context.models == (User, Order)

   def test_dispatch_method_added(self, mock_adapter):
       """Test _dispatch method is added by decorator"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       assert hasattr(context, '_dispatch')
       assert callable(context._dispatch)

   def test_operation_methods_call_dispatch(self, mock_adapter):
       """Test generated operation methods call _dispatch"""

       # Track if _dispatch was called
       dispatch_calls = []

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       # Override _dispatch after initialization
       original_dispatch = context._dispatch
       def mock_dispatch(opname, *args, **kwargs):
           dispatch_calls.append((opname, args, kwargs))
           return f"dispatched_{opname}"

       context._dispatch = mock_dispatch

       # Test that calling operation method calls _dispatch
       result = context.add("test_arg")

       assert result == "dispatched_add"
       assert len(dispatch_calls) == 1
       assert dispatch_calls[0][0] == "add"
       assert dispatch_calls[0][1] == ("test_arg",)

   def test_agnostic_operations_dispatch(self, mock_adapter):
       """Test agnostic operations (add/update/delete) dispatch correctly"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       with context as mgr:
           user = User(id=1, name="Test")

           # These should work via _getmanager -> manager.operation
           result = mgr.add(user)
           assert result == user
           assert user in mock_adapter.added_items

   def test_custom_operations_dispatch_to_model(self, mock_adapter):
       """Test custom operations dispatch to model class methods"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       with context as mgr:
           # This should call User.GetOrders(session, user_id)
           result = mgr.GetOrders(123)
           assert result == ["Order for user 123"]

   def test_dispatch_no_args_raises_error(self, mock_adapter):
       """Test dispatch with no args raises error"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       with context as mgr:
           with pytest.raises(ValueError):
               mgr._dispatch("add")

   def test_dispatch_unknown_operation_raises_error(self, mock_adapter):
       """Test dispatch with unknown operation raises error"""

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User)

       with context as mgr:
           with pytest.raises(AttributeError):
               mgr._dispatch("unknown_operation", "arg")

   def test_doesnt_override_existing_methods(self, mock_adapter):
       """Test decorator doesn't override existing methods"""

       @registeroperations
       class TestContext(ManagerContext):
           def add(self, item):
               return "custom_add"

       context = TestContext(mock_adapter, User)

       # Should keep custom add method
       result = context.add("test")
       assert result == "custom_add"

   def test_multiple_models_custom_operations(self, mock_adapter):
       """Test custom operations from multiple models"""

       # Add custom operation to Order
       Order.__super__ = {'GetItems'}
       Order.GetItems = classmethod(lambda cls, session, order_id: [f"Item for order {order_id}"])

       @registeroperations
       class TestContext(ManagerContext):
           pass

       context = TestContext(mock_adapter, User, Order)

       # Should have operations from both models
       assert hasattr(context, 'GetOrders')    # From User
       assert hasattr(context, 'GetAddresses') # From User
       assert hasattr(context, 'GetItems')     # From Order
