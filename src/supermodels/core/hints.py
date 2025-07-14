# ~/supermodels/src/supermodels/core/hints.py
"""
Type Hints and Aliases

Common type aliases used throughout the supermodels package for better
type safety and code readability.
"""
from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from supermodels.core.bases.manager import BaseManager

MetaModelRegistry = t.Dict[t.Type[t.Any], t.Type['BaseManager']]

ManagerInstanceRegistry = t.Dict[t.Type[t.Any], 'BaseManager']
