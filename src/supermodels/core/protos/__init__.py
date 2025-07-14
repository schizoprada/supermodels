# ~/supermodels/src/supermodels/core/protos/__init__.py
"""
Protocols

Protocol definitions for type checking and interface compliance.
Ensures compatibility across different database frameworks and model types.
"""

from .database import DBSession, DictableModel, JsonableModel, SerializableModel

__all__ = ['DBSession', 'DictableModel', 'JsonableModel', 'SerializableModel']
