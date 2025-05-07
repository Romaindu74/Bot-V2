from Slazhe import Logger
Log = Logger(__name__)

from Slazhe.Modules import importer
if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

from threading  import Thread
from typing     import Any, Dict, Callable

import json, os
import discord, asyncio
from pathlib import Path
from discord.ext import commands

from .Prefixes  import Prefixes
from .Listeners import Listeners
from .Commands  import CogLoader

# --- SlazheBot class ---
class SlazheBot:
    def __init__(self, uuid: str) -> None:
        Log.Debug(f"Initializing bot with UUID: {uuid}")
        
        if not hasattr(importer, "Storage") or importer.Storage is None:
            Log.Critical("Storage module is not available.")
            raise RuntimeError("Storage module is not available.")

        # Bot state variables
        self.__started: bool = False
        self.__stopped: bool = False
        self.__is_ready: bool = False

        # Unique identifier and storage
        self.__uuid: str = uuid
        self.__Storage: TypingStorage = importer.Storage(
            f"var/Slazhe-Bots/{self.__uuid}/", self.__uuid,
            self.__save_storage, self.__open_storage, True
        )

        # Bot information
        self.__information: dict[str, Any] = self.__Storage.open("main.slze", {})
        if not self.__information:
            Log.Critical(f"Missing information for bot {self.__uuid}")
            raise ValueError(f"Missing information for bot {self.__uuid}")

        # Token validation
        self.__token: str = self.__information.get("token")
        if not self.__token:
            Log.Critical(f"Missing token for bot {self.__uuid}")
            raise ValueError(f"Missing token for bot {self.__uuid}")

        self.__path_CogLoader: str = os.path.join(__file__.split(__name__.replace(".", "\\") + ".py")[0], "Slazhe", "Discord", "Files")

        # Bot setup (prefixes and listeners)
        self.__bot_prefixes: Prefixes = Prefixes(self)
        self.__bot_listeners: Listeners = Listeners(self)
        self.__bot_cogloader: CogLoader = CogLoader(
            self, self.__path_CogLoader
        )

        # Event listeners
        self.__uuid_connect_event: str = self.__bot_listeners.add_event_listener("on_connect", self.__on_connect)
        self.__uuid_ready_event: str = self.__bot_listeners.add_event_listener("on_ready", self.__on_ready)

        self.__loop: asyncio.AbstractEventLoop = None


    # --- Discord Client Configuration ---
    def __configure_discord_client(self) -> None:
        Log.Debug("Configuring Discord client...")

        self.__discord_client = commands.Bot(
            command_prefix=self.__bot_prefixes.run,
            intents=discord.Intents.all()
        )
        self.__intents_enabled: bool = True

        self.add_cog = self.__bot_cogloader.add_cog
        Log.Info("Discord client configured with all intents.")

    # --- Properties ---
    @property
    def name(self) -> str:
        return self.__information.get("name", "Unknown")
    
    @name.setter
    def name(self, value: str) -> None:
        Log.Debug(f"Setting bot name: {value}")
        self.__information["name"] = value

    @property
    def id(self) -> str:
        return self.__information.get("id", "Unknown")

    @id.setter
    def id(self, value: str) -> None:
        Log.Debug(f"Setting bot ID: {value}")
        self.__information["id"] = value

    @property
    def uuid(self) -> str:
        return self.__uuid
    
    @property
    def intents_enable(self) -> bool:
        return self.__intents_enabled

    @property
    def bot(self) -> commands.Bot:
        return self.__discord_client

    @property
    def started(self) -> bool:
        return self.__started
    
    @property
    def is_ready(self) -> bool:
        return self.__is_ready

    def add_listener(self, func: Callable, name: str) -> None:
        self.__bot_listeners.add_event_listener(name, func)

    # --- Module Loading ---
    async def __load_modules(self) -> None:
        Log.Debug("Loading modules...")
        try:
            await self.__bot_listeners.bot_add_cog()
            await self.__bot_cogloader.load_cogs()
            Log.Info("Modules loaded successfully.")
        except Exception as e:
            Log.Error(f"Failed to load modules: {e}")
            raise

    # --- Exception Handling ---
    def __handle_async_exception(self, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        exc = context.get('exception')
        if isinstance(exc, discord.ConnectionClosed):
            Log.Warning(f"Discord connection closed: {exc}")
        else:
            Log.Error(f"{self.__uuid}, Unhandled exception in event loop: {context}")

    # --- Main Async Task ---
    async def __async_main(self) -> None:
        Log.Debug("Starting bot main asynchronous task...")
        try:
            await self.__load_modules()
            Log.Info("Starting bot with token.")
            await self.__discord_client.start(self.__token)
        except asyncio.CancelledError:
            Log.Info("Bot shutdown requested.")
        except discord.errors.PrivilegedIntentsRequired:
            Log.Warning("Privileged intents not enabled, using default intents.")
            self.__discord_client = commands.Bot(
                command_prefix=self.__bot_prefixes.run,
                intents=discord.Intents.default()
            )
            self.__intents_enabled: bool = False

            await self.__async_main()
        except Exception as e:
            Log.Critical(f"Fatal error in bot main task: {e}")
            raise

    # --- Loop and Shutdown Handling ---
    async def __clear_loop(self) -> None:
        Log.Debug("Clearing all tasks from event loop...")
        tasks = [t for t in asyncio.all_tasks(self.__loop) if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        if not self.__loop.is_closed():
            self.__loop.stop()
            self.__loop.close()

    async def __shutdown(self) -> None:
        Log.Info(f"Shutting down bot {self.__uuid}...")
        if not self.__discord_client.is_closed():
            try:
                await self.__discord_client.close()
            except asyncio.TimeoutError:
                Log.Warning(f"Timeout while closing Discord client for bot {self.__uuid}")
            except Exception as e:
                Log.Error(f"Unexpected error while closing Discord client: {e}")

        await self.__clear_loop()

        Log.Info(f"Bot {self.__uuid} stopped.")

    def __run_async(self) -> None:
        Log.Debug("Running bot asynchronously...")
        self.__loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__loop)
        self.__loop.set_exception_handler(self.__handle_async_exception)

        self.__loop.run_until_complete(self.__async_main())

    # --- Bot Start and Stop ---
    def start(self) -> None:
        Log.Debug(f"Attempting to start bot {self.__uuid}...")
        if self.__started:
            Log.Warning(f"Bot {self.__uuid} is already started.")
            return

        self.__configure_discord_client()

        self.__started = True
        self.__stopped = False
        self.__is_ready = False

        Thread(
            target=self.__run_async,
            name=f"Bot-{self.__uuid}",
            daemon=True
        ).start()

        Log.Info(f"Bot {self.__uuid} starting...")

    def stop(self) -> None:
        Log.Debug(f"Attempting to stop bot {self.__uuid}...")
        if not self.__started or self.__stopped:
            Log.Warning(f"Bot {self.__uuid} is already stopped.")
            return

        self.__started = self.__is_ready = False
        self.__stopped = True
        if self.__loop and self.__loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.__shutdown(), self.__loop)
            try:
                future.result(10)
            except asyncio.TimeoutError:
                Log.Warning(f"Timeout during bot shutdown.")
            except Exception as e:
                Log.Error(f"Error during bot shutdown: {e}")

        Log.Info(f"Bot {self.__uuid} stopping...")

    # --- Event Listeners ---
    async def __on_ready(self) -> None:
        self.__is_ready = True
        Log.Info(f"Bot {self.__uuid} is ready!")
        
        if self.__stopped and self.__loop and self.__loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.__shutdown(), self.__loop)
            try:
                future.result(10)
            except asyncio.TimeoutError:
                Log.Warning(f"Timeout during bot shutdown.")
            except Exception as e:
                Log.Error(f"Error during bot shutdown: {e}")

            Log.Info(f"Bot {self.__uuid} stopping...")

        if self.__discord_client.user:
            self.name = self.__discord_client.user.name
            self.id   = self.__discord_client.user.id

            self.save()

        self.__bot_cogloader.sync(self.__token)
        for guild in self.__discord_client.guilds:
            self.__bot_cogloader.sync(self.__token, guild.id)

    async def __on_connect(self) -> None:
        Log.Info(f"Bot {self.__uuid} connected to Discord.")

    # --- Storage Handling ---
    @staticmethod
    def __open_storage(data: str) -> Dict[str, Any]:
        try:
            Log.Debug("Opening storage data...")
            return json.loads(data)
        except json.JSONDecodeError as e:
            Log.Error(f"Failed to decode storage data: {e}")
            return {}
        except Exception as e:
            Log.Error(f"Unexpected error opening storage: {e}")
            return {}

    @staticmethod
    def __save_storage(data: Dict[str, Any]) -> str:
        Log.Debug("Saving storage data...")
        return json.dumps(data)

    def save(self) -> bool:
        Log.Info("Saving bot data...")
        return self.__Storage.save(self.__information, "main.slze")

# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.55
