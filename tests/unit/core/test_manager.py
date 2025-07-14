# ~/supermodels/tests/unit/core/test_manager.py
import pytest
from supermodels.core.manager import Manager, ManagerContext
from supermodels.core.metas.manager import ManagerMeta
from tests.fixtures.models import User, Order
from tests.fixtures.adapters import MockAdapter
from tests.fixtures.managers import UserManager, OrderManager

class TestManager:

    def test_manager_creation(self, mock_adapter):
        """Test Manager instantiation"""
        manager = Manager(mock_adapter)
        assert manager.adapter == mock_adapter

    def test_call_with_single_model(self, mock_adapter):
        """Test Manager call with single model"""
        manager = Manager(mock_adapter)
        context = manager(User)

        assert isinstance(context, ManagerContext)
        assert User in context.models

    def test_call_with_multiple_models(self, mock_adapter):
        """Test Manager call with multiple models"""
        manager = Manager(mock_adapter)
        context = manager(User, Order)

        assert isinstance(context, ManagerContext)
        assert User in context.models
        assert Order in context.models

    def test_call_with_no_models_raises_error(self, mock_adapter):
        """Test Manager call with no models raises error"""
        manager = Manager(mock_adapter)

        with pytest.raises(ValueError):
            manager()

    def test_call_with_duplicate_models_raises_error(self, mock_adapter):
        """Test Manager call with duplicate models raises error"""
        manager = Manager(mock_adapter)

        with pytest.raises(ValueError):
            manager(User, User)

    def test_call_with_unregistered_model_raises_error(self, mock_adapter):
        """Test Manager call with unregistered model raises error"""
        class UnregisteredModel:
            pass

        manager = Manager(mock_adapter)

        with pytest.raises(ValueError):
            manager(UnregisteredModel)

class TestManagerContext:

    def test_context_creation(self, mock_adapter):
        """Test ManagerContext creation"""
        context = ManagerContext(mock_adapter, User, Order)

        assert context.adapter == mock_adapter
        assert context.models == (User, Order)
        assert context.session is None
        assert context._managersregistry == {}

    def test_context_enter_creates_session(self, mock_adapter):
        """Test entering context creates session and managers"""
        context = ManagerContext(mock_adapter, User, Order)

        with context as mgr:
            assert mgr.session is not None
            assert User in mgr._managersregistry
            assert Order in mgr._managersregistry
            assert isinstance(mgr._managersregistry[User], UserManager)
            assert isinstance(mgr._managersregistry[Order], OrderManager)

    def test_context_exit_closes_session(self, mock_adapter):
        """Test exiting context closes session"""
        context = ManagerContext(mock_adapter, User)

        with context as mgr:
            session = mgr.session

        assert session.closed

    def test_context_exit_rollback_on_exception(self, mock_adapter):
        """Test context rollback on exception"""
        context = ManagerContext(mock_adapter, User)

        try:
            with context as mgr:
                session = mgr.session
                raise RuntimeError("Test error")
        except RuntimeError:
            pass

        assert session.rolled_back
        assert session.closed

    def test_getmanager_direct_match(self, mock_adapter):
        """Test _getmanager with direct type match"""
        context = ManagerContext(mock_adapter, User, Order)

        with context as mgr:
            user = User(id=1)
            manager = mgr._getmanager(user)
            assert isinstance(manager, UserManager)

    def test_getmanager_inheritance_match(self, mock_adapter):
        """Test _getmanager with inheritance"""
        class SpecialUser(User):
            pass

        context = ManagerContext(mock_adapter, User)

        with context as mgr:
            special_user = SpecialUser(id=1)
            manager = mgr._getmanager(special_user)
            assert isinstance(manager, UserManager)

    def test_getmanager_no_match_raises_error(self, mock_adapter):
        """Test _getmanager with no match raises descriptive error"""
        context = ManagerContext(mock_adapter, User)

        with context as mgr:
            order = Order(id=1)

            with pytest.raises(ValueError):
                mgr._getmanager(order)

    def test_getmanager_none_item_raises_error(self, mock_adapter):
        """Test _getmanager with None raises error"""
        context = ManagerContext(mock_adapter, User)

        with context as mgr:
            with pytest.raises(ValueError):
                mgr._getmanager(None)
