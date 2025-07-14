# ~/supermodels/tests/fixtures/models.py
class User:
    __super__ = {'GetOrders', 'GetAddresses'}

    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def GetOrders(cls, session, user_id):
        return [f"Order for user {user_id}"]

    @classmethod
    def GetAddresses(cls, session, user_id):
        return [f"Address for user {user_id}"]

class Order:
    def __init__(self, id=None, user_id=None, amount=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
