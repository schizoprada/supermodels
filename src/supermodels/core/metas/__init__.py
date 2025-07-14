# ~/supermodels/src/supermodels/core/metas/__init__.py
"""
Metaclasses

Metaclass definitions for automatic registration and configuration.
Provides the foundation for dynamic model-to-manager mapping.
"""

from .manager import ManagerMeta

__all__ = ['ManagerMeta']
