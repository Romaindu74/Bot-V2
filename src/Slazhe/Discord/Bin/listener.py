from .utils import _BaseListener

from .cog import Cog as CogT

from typing import Callable, Any, Self, Optional

import asyncio

class Listener(_BaseListener):
    __original_kwargs__: dict[str, Any]

    def __new__(cls, *args: Any, **kwargs: Any):
        self = super().__new__(cls)
        
        self.__original_kwargs__ = kwargs.copy()

        return self

    def __init__(self, func: Callable, **kwargs: Any) -> None:
        self.kw: dict[str, Any]     = kwargs
        self.iscoroutinefunc: bool  = asyncio.iscoroutinefunction(func)

        name = kwargs.get('name') or func.__name__
        if not isinstance(name, str):
            raise TypeError('Name of a command must be a string.')
        self.name: str = name

        self.callback: Callable = func
        self.__cog: CogT        = None

    @property
    def cog(self) -> Optional[CogT]:
        return self.__cog
    
    @cog.setter
    def cog(self, value: CogT) -> None:
        self.__cog = value
    def copy(self) -> Self:
        """Creates a copy of this command.

        Returns
        --------
        :class:`Command`
            A new instance of this command.
        """
        return self.__class__(self.callback, **self.__original_kwargs__)

    def _update_copy(self, kwargs: dict[str, Any]) -> Self:
        if kwargs:
            kw = kwargs.copy()
            kw.update(self.__original_kwargs__)
            return self.__class__(self.callback, **kw)
        else:
            return self.copy()

    async def invoke(self, /, *args: Any,**kwargs: Any) -> Any:
        if self.cog is not None:
            if self.iscoroutinefunc:
                return await self.callback(self.cog, *args, **kwargs)
            return self.callback(self.cog, *args, **kwargs)
        else:
            if self.iscoroutinefunc:
                return await self.callback(*args, **kwargs)
            return self.callback(*args, **kwargs)


def listener(
    name: str = None,
    **attrs: Any,
) -> Any:
    def decorator(func):
        if isinstance(func, Listener):
            raise TypeError('Callback is already a listener.')
        return Listener(func, name=name, **attrs)

    return decorator
# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.09
