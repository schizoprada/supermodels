# ~/supermodels/src/supermodels/core/models/tvars.py
"""
typing.TypeVars
"""
from __future__ import annotations
import typing as t

T = t.TypeVar('T')

SessionProtoType = t.TypeVar('SessionProtoType', covariant=True)
SessionType = t.TypeVar('SessionType')

ModelType = t.TypeVar('ModelType')
