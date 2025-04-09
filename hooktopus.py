__all__ = ["loader"]

from typing import Type, Iterable, Generic, TypeVar
import inspect
import pkg_resources
import itertools


_T = TypeVar("T")


class _PluginProvider(Generic[_T]):

    def __init__(self, klass: Type[_T]):
        self._klass = klass

    def using(self, *args: str) -> Iterable[Type[_T]]:
        """
        Use the given entrypoint to create a plugin provider.
        """
        for ep in itertools.chain(map(pkg_resources.iter_entry_points, args)):
            klass = ep.load()
            if not inspect.isclass(klass) or not issubclass(klass, self._klass):
                continue
            yield klass


loader = _PluginProvider
