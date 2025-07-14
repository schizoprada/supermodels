# ~/supermodels/tests/unit/core/metas/test_manager.py
# tests/unit/core/metas/test_manager.py
import pytest
from supermodels.core.metas.manager import ManagerMeta
from supermodels.core.bases.manager import BaseManager
from tests.fixtures.models import User, Order

class TestManagerMeta:

    def test_single_model_registration(self):
        """Test manager with single model gets registered"""
        class TestManager(BaseManager, metaclass=ManagerMeta):
            __model__ = User

        # Check registration
        assert ManagerMeta.GetModelManager(User) == TestManager
        assert User in ManagerMeta.GetRegistry()

    def test_multiple_models_registration(self):
        """Test manager with multiple models gets registered"""
        class MultiManager(BaseManager, metaclass=ManagerMeta):
            __models__ = (User, Order)

        # Check both models registered to same manager
        assert ManagerMeta.GetModelManager(User) == MultiManager
        assert ManagerMeta.GetModelManager(Order) == MultiManager
        assert User in ManagerMeta.GetRegistry()
        assert Order in ManagerMeta.GetRegistry()

    def test_instance_manager_lookup(self):
        """Test getting manager by instance"""
        class UserManager(BaseManager, metaclass=ManagerMeta):
            __model__ = User

        user = User(id=1, name="Test")
        assert ManagerMeta.GetInstanceMangager(user) == UserManager

    def test_get_manager_with_type(self):
        """Test GetManager with type"""
        class UserManager(BaseManager, metaclass=ManagerMeta):
            __model__ = User

        assert ManagerMeta.GetManager(User) == UserManager

    def test_get_manager_with_instance(self):
        """Test GetManager with instance"""
        class UserManager(BaseManager, metaclass=ManagerMeta):
            __model__ = User

        user = User(id=1)
        assert ManagerMeta.GetManager(user) == UserManager

    def test_no_model_raises_error(self):
        """Test manager without model/models raises error"""
        with pytest.raises(AttributeError):
            class BadManager(BaseManager, metaclass=ManagerMeta):
                pass

    def test_empty_models_raises_error(self):
        """Test manager with empty models raises error"""
        with pytest.raises(AttributeError):
            class BadManager(BaseManager, metaclass=ManagerMeta):
                __models__ = ()

    def test_registry_copy(self):
        """Test GetRegistry returns copy"""
        class TestManager(BaseManager, metaclass=ManagerMeta):
            __model__ = User

        registry = ManagerMeta.GetRegistry()
        original_size = len(registry)

        # Modify copy
        registry.clear()

        # Original registry unchanged
        assert len(ManagerMeta.GetRegistry()) == original_size
