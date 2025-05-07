from typing import Any, Callable, Self, Optional
from .utils import _BaseCommand

from discord.app_commands.commands      import _extract_parameters_from_callback
from discord.app_commands.transformers  import CommandParameter
from discord.enums                      import AppCommandType, AppCommandOptionType
from discord.permissions                import Permissions

from .cog       import Cog as CogT
from .context   import Context

import asyncio

class Command(_BaseCommand):
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
        self.callback: Callable = func
        self.description: str   = kwargs.get('description', '.')
        self.enabled: bool      = kwargs.get('enabled', True)
        self.aliases: list[str] = kwargs.get('aliases', [])
        self.name: str          = name
        self.nsfw: bool         = kwargs.get('nsfw', False)

        self.guild_ids: list[int] = kwargs.get('guild_ids', None)

        self.ephemeral: bool    = kwargs.get('ephemeral', False)
        self.typing: bool       =  kwargs.get('typing', True)

        self.parent: Optional[Any] = kwargs.get('parent', None)

        self.beffore: list[Callable] = kwargs.get('beffore', [])
        self.after:   list[Callable] = kwargs.get('after', [])

        self.default_member_permissions: int    = kwargs.get('default_member_permissions', None)
        self.dm_permission: bool                = kwargs.get('dm_permission', True)
        self.msg_charging: bool                 = kwargs.get('msg_charging', True)

        self.guild_only: bool                       = kwargs.get('guild_only', False)
        self._params: dict[str, CommandParameter]   = _extract_parameters_from_callback(func, func.__globals__)
        self.default_permissions: Optional[Permissions] = getattr(
            func, '__discord_app_commands_default_permissions__', None
        )

        self.check: bool    = False
        self.__cog: CogT     = None

    @property
    def cog(self) -> Optional[CogT]:
        return self.__cog
    
    @cog.setter
    def cog(self, value: CogT) -> None:
        self.__cog = value

    @property
    def to_dict(self) -> dict[str, Any]:
        option_type = AppCommandType.chat_input.value if self.parent is None else AppCommandOptionType.subcommand.value
        base: dict[str, Any] = {
            'name': self.name,
            'description': self.description,
            'type': option_type,
            'options': [param.to_dict() for param in self._params.values()],
        }

        if self.parent is None:
            base['nsfw'] = self.nsfw
            base['dm_permission'] = not self.guild_only
            base['default_member_permissions'] = None if self.default_permissions is None else self.default_permissions.value

        return base

    @property
    def info(self) -> dict[str, Any]:
        data = self.to_dict.copy()

        del data["type"]
        del data["options"]

        if self.parent is None:
            del data["dm_permission"]
            del data['default_member_permissions']

        return data

    async def __call__(self, context: Any, /, *args: Any,**kwargs: Any) -> Any:
        if self.cog is not None:
            if self.iscoroutinefunc:
                return await self.callback(self.cog, context, *args, **kwargs)
            return self.callback(self.cog, context, *args, **kwargs)
        else:
            if self.iscoroutinefunc:
                return await self.callback(self.cog, context, *args, **kwargs)
            return self.callback(context, *args, **kwargs)

    @property
    def cog_name(self) -> Optional[str]:
        return type(self.cog).__cog_name__ if self.cog is not None else None

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

    async def invoke_beffore(self, ctx: Context, *args: Any, **kwargs: Any) -> None:
        if self.beffore is None:
            return

        self._invoke_list(self.beffore, ctx, *args, **kwargs)

    async def invoke_after(self, ctx: Context, *args: Any, **kwargs: Any) -> None:
        if self.after is None:
            return
        
        self._invoke_list(self.after, ctx, *args, **kwargs)

    async def _invoke_list(self, functions: list[Callable], ctx: Context, *args: Any, **kwargs: Any) -> None:
        for function in functions:
            try:
                await function(ctx, *args, **kwargs)

            except Exception as e:
                print(f'Error in command {function.__name__}: {e}')

def command(
    name: str = None,
    **attrs: Any,
) -> Any:
    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return Command(func, name=name, **attrs)

    return decorator
# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.0q
