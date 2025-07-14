# ~/supermodels/tests/fixtures/managers.py
from supermodels.core.bases.manager import BaseManager
from tests.fixtures.models import User, Order

class UserManager(BaseManager):
    __model__ = User

class OrderManager(BaseManager):
    __model__ = Order
