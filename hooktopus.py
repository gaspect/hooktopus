__all__ = ["plugins"]

import inspect
from importlib import metadata
from typing import Type, Iterable


class Plugins[T]:
    """
    A plugin provider that uses entry points to load plugins.
    """

    def __init__(self, klass: Type[T]):
        super().__init__()
        self._klass = klass

    @classmethod
    def of(cls, klass: Type[T]) -> "Plugins[T]":
        return cls(klass)

    def using(self, *args: str) -> Iterable[Type[T]]:
        """
        Iterate over all plugins.
        """
        for group in args:
            eps = metadata.entry_points(group=group)
            for name in eps.names:
                klass = eps[name].load()
                if inspect.isclass(klass) and issubclass(klass, self._klass):
                    yield klass
