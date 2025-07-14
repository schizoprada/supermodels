# ~/supermodels/tests/conftest.py
import pytest
from tests.fixtures.models import User, Order
from tests.fixtures.managers import UserManager, OrderManager
from tests.fixtures.adapters import MockAdapter

@pytest.fixture
def mock_adapter():
    return MockAdapter()

@pytest.fixture
def sample_user():
    return User(id=1, name="Test User", email="test@example.com")

@pytest.fixture
def sample_order():
    return Order(id=1, user_id=1, amount=100.0)

@pytest.fixture
def sample_models():
    return (User, Order)
