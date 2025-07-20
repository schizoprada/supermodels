# ~/supermodels/src/supermodels/adapters/sqla/typer.py
"""
...
"""
from __future__ import annotations
import typing as t

from sqlalchemy.types import TypeDecorator, JSON

from supermodels.converters.base import BaseConverter, ConversionTarget, ConversionOptions

class SQLATypeAdapter(TypeDecorator):
    """
    ...
    """
    impl = JSON
    cache_ok = True

    def __init__(
        self,
        converter: t.Type[BaseConverter],
        targeting: ConversionTarget,
        **options: ConversionOptions
    ) -> None:
        """..."""
        super().__init__()
        self.converter: BaseConverter = converter(targeting, **options)

    def compare_against_backend(self, dialect, conn_type):
        """..."""
        return isinstance(conn_type, JSON)

    def process_bind_param(self, value, dialect) -> t.Any:
        """..."""
        if value is None:
            return None
        return self.converter.serialize(value)

    def process_result_value(self, value, dialect):
        """..."""
        if value is None:
            return None
        return self.converter.deserialize(value)

    @classmethod
    def Dataclasses(cls, targeting: ConversionTarget, **options: t.Any) -> 'SQLATypeAdapter':
        """..."""
        from supermodels.converters.dc import DataclassConverter
        return cls(
            converter=DataclassConverter,
            targeting=targeting,
            **options
        )

    @classmethod
    def Pydantic(cls, targeting: ConversionTarget, **options: t.Any) -> 'SQLATypeAdapter':
        """..."""
        from supermodels.converters.pyd import PydanticConverter
        return cls(
            converter=PydanticConverter,
            targeting=targeting,
            **options
        )


DCType: t.Callable = SQLATypeAdapter.Dataclasses
PydType: t.Callable = SQLATypeAdapter.Pydantic
