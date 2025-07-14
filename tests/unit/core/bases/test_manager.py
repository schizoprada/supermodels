# ~/supermodels/tests/unit/core/bases/test_manager.py
import pytest
from supermodels.core.bases.manager import BaseManager
from supermodels.core.metas.manager import ManagerMeta
from tests.fixtures.models import User, Order
from tests.fixtures.adapters import MockAdapter

class TestBaseManager:

    def test_manager_creation(self, mock_adapter):
        """Test basic manager instantiation"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)

        assert manager.session == session
        assert manager.adapter == mock_adapter

    def test_add_operation(self, mock_adapter):
        """Test add operation delegates to adapter"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)
        user = User(id=1, name="Test")

        result = manager.add(user)

        assert result == user
        assert user in mock_adapter.added_items
        assert session.committed

    def test_update_operation(self, mock_adapter):
        """Test update operation delegates to adapter"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)
        user = User(id=1, name="Updated")

        result = manager.update(user)

        assert result == user
        assert user in mock_adapter.updated_items

    def test_delete_operation(self, mock_adapter):
        """Test delete operation delegates to adapter"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)
        user = User(id=1)

        result = manager.delete(user)

        assert result is True
        assert user in mock_adapter.deleted_items

    def test_get_with_model_provided(self, mock_adapter):
        """Test get operation with explicit model"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)

        result = manager.get(User, 1)

        assert isinstance(result, User)
        assert result.id == 1

    def test_get_with_default_model(self, mock_adapter):
        """Test get operation using default model"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)

        result = manager.get(None, 1)

        assert isinstance(result, User)
        assert result.id == 1

    def test_get_without_model_raises_error(self, mock_adapter):
        """Test get operation without model raises error"""
        class NoModelManager(BaseManager):
            __model__ = User

        NoModelManager.__model__ = None
        session = mock_adapter.createsession()
        manager = NoModelManager(session, mock_adapter)

        with pytest.raises(ValueError):
            manager.get(None, 1)

    def test_getinstancemodel_direct_match(self, mock_adapter):
        """Test _getinstancemodel with direct type match"""
        class UserManager(BaseManager):
            __models__ = (User, Order)

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)
        user = User(id=1)

        result = manager._getinstancemodel(user)

        assert result == User

    def test_getinstancemodel_inheritance_match(self, mock_adapter):
        """Test _getinstancemodel with inheritance"""
        class SpecialUser(User):
            pass

        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)
        special_user = SpecialUser(id=1)

        result = manager._getinstancemodel(special_user)

        assert result == User

    def test_getinstancemodel_no_match_raises_error(self, mock_adapter):
        """Test _getinstancemodel with no match raises error"""
        class UserManager(BaseManager):
            __model__ = User

        session = mock_adapter.createsession()
        manager = UserManager(session, mock_adapter)
        order = Order(id=1)

        with pytest.raises(ValueError):
            manager._getinstancemodel(order)
