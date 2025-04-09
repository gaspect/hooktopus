__all__ = ["plugins"]

import inspect
import itertools
import pkg_resources
from typing import Type, Iterable


class _PluginProvider[T]:
    """
    A plugin provider that uses entry points to load plugins.
    """

    def __init__(self, klass: Type[T]):
        super().__init__()
        self._klass = klass

    def using(self, *args: str) -> Iterable[Type[T]]:
        """
        Iterate over all plugins.
        """
        for entry_point in itertools.chain(map(pkg_resources.iter_entry_points, args)):
            klass = entry_point.load()
            if inspect.isclass(klass) and (issubclass(klass, T) or klass is T):
                yield klass


plugins = _PluginProvider
