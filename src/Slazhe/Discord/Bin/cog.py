from typing import Any, Self

from .utils import _BaseCommand, _BaseListener

import inspect

class CogMeta(type):
    __cog_name__:           str
    __cog_description__:    str
    __cog_group__:          bool
    __cog_listeners__:      dict[str, _BaseListener]
    __cog_commands__:       dict[str, _BaseCommand]
    __cog_settings__:       dict[str, Any]

    def __new__(cls, *args: Any, **kwargs: Any) -> 'CogMeta':
        name, bases, attrs = args

        try:
            cog_name = kwargs.pop('name')
        except KeyError:
            cog_name = name

        attrs['__cog_name__'] = cog_name

        description = kwargs.pop('description', None)
        if description is None:
            description = inspect.cleandoc(attrs.get('__doc__', '...'))

        attrs['__cog_description__']    = description
        attrs['__cog_settings__']       = kwargs.pop('command_attrs', {})
        attrs['__cog_group__']          = kwargs.pop("group", False)

        listeners:      dict[str, _BaseListener]    = {}
        commands:       dict[str, _BaseCommand]     = {}

        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)
        for base in reversed(new_cls.__mro__):
            for elem, value in base.__dict__.items():
                if elem in commands:
                    del commands[elem]
                if elem in listeners:
                    del listeners[elem]

                if isinstance(value, _BaseCommand):
                    commands[elem] = value
                if isinstance(value, _BaseListener):
                    listeners[elem] = value

        new_cls.__cog_listeners__   = listeners
        new_cls.__cog_commands__    = commands

        return new_cls

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)

class Cog(metaclass=CogMeta):
    __cog_name__:           str
    __cog_description__:    str
    __cog_group__:          bool
    __cog_listeners__:      dict[str, _BaseListener]
    __cog_commands__:       dict[str, _BaseCommand]
    __cog_settings__:       dict[str, Any]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        self = super().__new__(cls)
        cmd_attrs = cls.__cog_settings__

        self.__cog_commands__       = {c.name: c._update_copy(cmd_attrs) for n, c in cls.__cog_commands__.items()}
        self.__cog_listeners__      = {c.name: c._update_copy(cmd_attrs) for n, c in cls.__cog_listeners__.items()}

        __cog_setters__ = []
        __cog_setters__.extend(self.__cog_commands__.values())
        __cog_setters__.extend(self.__cog_listeners__.values())
        
        for k in __cog_setters__:
            k.cog = self

        return self

    def any_listeners(self) -> dict[str, _BaseListener]:
        return self.__cog_listeners__

    def any_commands(self) -> dict[str, _BaseCommand]:
        return self.__cog_commands__
    
    def get_commands(self, guild: int = None) -> dict[str, _BaseCommand]:
        if guild:
            return {
                n: c for n, c in self.__cog_commands__.items() if c.guild_ids and guild in c.guild_ids
            }

        return {
            n: c for n, c in self.__cog_commands__.items() if c.guild_ids is None
        }

    @property
    def qualified_name(self) -> str:
        return self.__cog_name__
    
    def slash(self, guild: int = None) -> list[dict[str, Any]]:
        return [c.to_dict for c in self.get_commands(guild).values()]
# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.0t
