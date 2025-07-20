# ~/supermodels/src/supermodels/converters/base.py
"""
...
"""
from __future__ import annotations
import abc, typing as t

ConversionTarget = t.Type[t.Any]
ConversionOptions = t.Dict[str, t.Any]
DateTimeFields = t.Set[str]


class BaseConverter(abc.ABC):
    """..."""
    __datetimes__: DateTimeFields = set()

    def __init__(
        self,
        targeting: ConversionTarget,
        **options: t.Any
    ) -> None:
        """..."""
        self.targeting: ConversionTarget = targeting
        self.options: ConversionOptions = options


    @abc.abstractmethod
    def serialize(self, value: t.Any, **kwargs) -> t.Any:
        """..."""
        pass

    @abc.abstractmethod
    def deserialize(self, value: t.Any, **kwargs) -> t.Any:
        """..."""
        pass
