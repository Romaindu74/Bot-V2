from Slazhe import Logger

_log = Logger(__name__)

from Slazhe.Discord.Bin.cog     import Cog as CogT
from Slazhe.Discord.Bin.utils   import _BaseCommand
from Slazhe.Discord.Bin.callcommands import callcommands

from discord.ext    import commands
from typing         import TypeVar, Callable, Any
from pathlib        import Path

import importlib
import asyncio
import os

T = TypeVar('T')

from Slazhe.SlazheModules import importer

if hasattr(importer, 'SlashCommand'):
    from Slazhe.SlazheModules.routes import SlashCommand

class CogLoader:
    def __init__(
        self,
        Client: commands.Bot = None,
        cog_path: str = 'Bot/Cog/',
        file_filter: Callable[[str], bool] = lambda f: f.endswith('.py') and not f.startswith('_'),
        setup_attr: str = 'setup',
        verbose: bool = True,
        stop_on_error: bool = False
    ):
        self.__Client: commands.Bot = Client
        self.__cog_path: Path       = Path(cog_path)
        self.__file_filter: Callable[[str], bool] = file_filter
        self.__setup_attr: str      = setup_attr
        self.__verbose: bool        = verbose
        self.__stop_on_error: bool  = stop_on_error

        self.__cogs: dict[str, CogT] = {}
        self.__callcommands: callcommands = callcommands()

    async def _load_module(self, module_path: str, module_name: str) -> bool:
        try:
            if self.__verbose:
                _log.Info(f'Chargement du module {module_name}')
            
            module = importlib.import_module(module_path.replace(os.sep, ".").replace(".py", ""), package = "Slazhe.Discord.Files")
            
            if not hasattr(module, self.__setup_attr):
                _log.Warn(f"Le module {module_name} n'a pas d'attribut {self.__setup_attr}")
                return False
                
            setup_func = getattr(module, self.__setup_attr)
            if not await setup_func(self.__Client):
                _log.Warn(f"Le setup de {module_name} a échouer.")
                return False
                
            if self.__verbose:
                _log.Info(f"{module_name} a bien été importer.")
            return True
            
        except Exception as e:
            _log.Error(f"Erreur lors de l'import de {module_name}: {e}")
            if self.__stop_on_error:
                raise
            return False

    async def load_cogs(self) -> bool:
        """Charge tous les cogs valides"""
        if self.__Client is None:
            _log.Warn("La variable Client est manquant")
            return False

        if self.__verbose:
            _log.Info("Chargements des cogs.")
            
        if not self.__cog_path.exists():
            _log.Error(f"Le chemin des cogs n'existe pas: {self.__cog_path}")
            return False

        cog_files = [
            str(f.relative_to(self.__cog_path)) for f in self.__cog_path.rglob('*.py')
            if f.is_file() and self.__file_filter(f.name) and not f.name.startswith('_')
        ]

        if self.__verbose:
            _log.Info(f"Found {len(cog_files)} cogs to load")

        results = await asyncio.gather(*[
            self._load_module(f'.{stem}', stem)
            for stem in cog_files
        ], return_exceptions=not self.__stop_on_error)

        success = all(results)
        
        if self.__verbose and success:
            _log.Info(f"Les cogs on bien été charger")
            
        return success
    
    def add_cog(self, cog: CogT) -> None:
        name: str = cog.qualified_name

        if name in self.__cogs:
            _log.Error(f"Le cog {name} est déjà enregistrer.")
            raise

        self.__cogs[name] = cog

        for command in cog.any_commands().values():
            self.__callcommands.decorator(self.__Client.bot, command)

        for listener in cog.any_listeners().values():
            self.__Client.add_listener(listener.invoke, listener.name)

        return True

    def remove_cog(self, cog: CogT) -> None:
        name: str = cog.qualified_name
        if name in self.__cogs:
            del self.__cogs[name]

    def sync(self, Token: str, guild: int = None) -> None:
        payload: list[dict[str, Any]] = []
        for cog in self.__cogs.values():
            payload.extend(cog.slash(guild))

        if len(payload) == 0:
            return

        route: SlashCommand = importer.SlashCommand(self.__Client.id, Token)

        application_id: int = self.__Client.bot.application_id
        if guild is None:
            route.bulk_upsert_global_commands(application_id, payload)
        else:
            route.bulk_upsert_guild_commands(application_id, guild, payload)
# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.1p
