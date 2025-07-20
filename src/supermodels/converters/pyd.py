# ~/supermodels/src/supermodels/converters/pyd.py
"""
...
"""
from __future__ import annotations
import typing as t
from datetime import datetime

from pydantic import BaseModel as PydModel

from supermodels.converters.base import BaseConverter, DateTimeFields, ConversionTarget, ConversionOptions


class PydanticConverter(BaseConverter):
    """..."""

    def __init__(
        self,
        targeting: ConversionTarget,
        datetimes: t.Optional[DateTimeFields] = None,
        **options: t.Any
    ) -> None:
        """..."""
        super().__init__(targeting, **options)
        if datetimes is not None:
            self.__datetimes__ = self.__datetimes__ | datetimes


    def serialize(self, value: t.Any, **kwargs) -> t.Any:
        """..."""
        def convertvalue(val: t.Any) -> t.Any:
            if isinstance(val, PydModel):
                return val.model_dump()
            elif isinstance(val, list):
                return [convertvalue(item) for item in val]
            elif isinstance(val, dict):
                return {k: convertvalue(v) for k,v in val.items()}
            elif isinstance(val, (int, float, str, bool)):
                return val
            else:
                return str(val)

        return convertvalue(value)


    def deserialize(self, value: t.Any, **kwargs) -> t.Any:
        """..."""
        def convertvalue(val: t.Any) -> t.Any:
            if isinstance(val, dict):
                if self.__datetimes__ and any(k in val for k in self.__datetimes__):
                    for k in self.__datetimes__:
                        if (k in val) and (val[k] is not None) and (val[k].lower() != 'none'):
                            val[k] = datetime.fromisoformat(val[k])
                return {k: convertvalue(v) for k,v in val.items()}
            elif isinstance(val, list):
                return [convertvalue(item) for item in val]
            return val

        if isinstance(self.targeting, type) and issubclass(self.targeting, PydModel):
            if isinstance(value, list):
                return [self.targeting(**convertvalue(item)) for item in value]
            return self.targeting(**convertvalue(value))
        return value
