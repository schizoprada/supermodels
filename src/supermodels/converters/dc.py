# ~/supermodels/src/supermodels/converters/dc.py
"""
...
"""
from __future__ import annotations
import typing as t, dataclasses as dcs
from datetime import datetime

from supermodels.converters.base import BaseConverter, DateTimeFields, ConversionTarget, ConversionOptions

class DataclassConverter(BaseConverter):
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
            if dcs.is_dataclass(val) and not isinstance(val, type): return {k: convertvalue(getattr(val, k)) for k in dcs.asdict(val)}
            elif isinstance(val, list): return [convertvalue(item) for item in val]
            elif isinstance(val, (int, float, str, bool)): return val
            elif isinstance(val, dict): return {k: convertvalue(v) for k,v in val.items()}
            else: return str(val)

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

        if isinstance(self.targeting, type) and dcs.is_dataclass(self.targeting):
            if isinstance(value, list):
                return [self.targeting(**convertvalue(item)) for item in value]
            return self.targeting(**convertvalue(value))
        return value
