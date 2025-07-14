# ~/supermodels/src/supermodels/core/models/tvars.py
"""
Type Variables

Common type variables used throughout the supermodels package.
Provides consistent typing for generic classes and functions.
"""
from __future__ import annotations
import typing as t

T = t.TypeVar('T')

SessionProtoType = t.TypeVar('SessionProtoType', covariant=True)
SessionType = t.TypeVar('SessionType')

ModelType = t.TypeVar('ModelType')
