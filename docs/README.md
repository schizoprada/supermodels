# SUPERMODELS

Type-safe, framework-agnostic database managers with context management and dynamic method dispatch.

## Features

- **Context-managed database operations** - Automatic session handling with proper cleanup
- **Dynamic method dispatch** - `mgr.add(item)` automatically detects model type
- **Automatic model registration** - Managers register themselves via metaclass
- **Custom model operations** - Support for model-specific methods via `__super__`
- **Multiple database frameworks** - Currently supports SQLAlchemy, extensible to others
- **Type-safe interfaces** - Full IDE support with proper type hints
- **Advanced SQLAlchemy features** - Pagination, bulk operations, optimized queries

## Quick Start

```python
from supermodels import Manager
from supermodels.adapters import SQLA
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Integer)

# Create managers
class UserManager(BaseManager):
    __model__ = User

class OrderManager(BaseManager):
    __model__ = Order

# Setup database
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

# Use supermodels
manager = Manager(SQLA(engine))

with manager(User, Order) as mgr:
    # Add items - automatic model detection
    user = mgr.add(User(name="John", email="john@example.com"))
    order = mgr.add(Order(user_id=user.id, amount=100))

    # Update items
    user.name = "John Doe"
    mgr.update(user)

    # Get items
    found_user = mgr.get(User, user.id)
    orders = mgr.getby(Order, user_id=user.id)
```

## Custom Model Operations

Add custom methods to your models:

```python
class User(Base):
    __tablename__ = 'users'
    __super__ = {'GetOrders', 'GetActiveOrders'}  # Custom operations

    # ... columns ...

    @classmethod
    def GetOrders(cls, session, user_id):
        return session.query(Order).filter(Order.user_id == user_id).all()

    @classmethod
    def GetActiveOrders(cls, session, user_id):
        return session.query(Order).filter(
            Order.user_id == user_id,
            Order.status == 'active'
        ).all()

# Usage
with manager(User, Order) as mgr:
    orders = mgr.GetOrders(123)  # Calls User.GetOrders(session, 123)
    active = mgr.GetActiveOrders(123)
```

## Global Default Adapter

Set a global default for convenience:

```python
from supermodels import Manager
from supermodels.adapters import SQLA

# Set global default
Manager[SQLA(engine)]

# Now you can use Manager without explicit adapter
manager = Manager()
```

## Factory Methods

Use factory methods for common setups:

```python
# SQLAlchemy factory
manager = Manager.SQLA(engine)

with manager(User, Order) as mgr:
    # ... operations ...
```

## Advanced SQLAlchemy Features

```python
from supermodels.adapters.sqla import OrderBy, ASC, DESC

adapter = SQLA(engine)

with adapter.createsession() as session:
    # Pagination with sorting
    users, total = adapter.querypage(
        session, User,
        page=1, hits=10,
        sortby='created_at', orderby=DESC,
        active=True
    )

    # Bulk operations
    new_users = [User(name=f"User{i}") for i in range(100)]
    adapter.bulkadd(session, *new_users)
```

## Installation

```bash
pip3 install supermodels
```

## Requirements

- Python 3.13+
- SQLAlchemy 1.4+ (for SQLAlchemy adapter)
