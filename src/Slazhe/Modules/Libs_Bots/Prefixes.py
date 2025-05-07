from Slazhe import Logger

Log = Logger(__name__)

from Slazhe.Modules import importer

if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

from typing import Any, Dict

import json
import uuid

from datetime import datetime

from discord.ext import commands
import discord

class Prefixes:
    def __init__(self, client: Any):
        self.__Client: Any      = client
        self.__Client_uuid: str = client.uuid

        if not hasattr(importer, "Storage") or importer.Storage is None:
            raise ValueError("Storage is not available.")

        self.__Storage: TypingStorage = importer.Storage(f"var/Slazhe-Bots/{self.__Client_uuid}/Prefixes/", __file__, self.__save_storage, self.__open_storage)

    # ---------- Storage ----------

    @staticmethod
    def __open_storage(data: str) -> Dict[str, Any]:
        """Helper method to open storage data."""
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            Log.Error(f"Failed to decode storage data: {e}")
            return {}
        except Exception as e:
            Log.Error(f"Unexpected error opening storage: {e}")
            return {}

    @staticmethod
    def __save_storage(data: Dict[str, Any]) -> str:
        """Helper method to save storage data."""
        return json.dumps(data)

    # ---------- Add ----------

    def __add_prefix(self, file: str, prefix: str, create_at: str, created_by: str, active: bool) -> bool:
        prefixes: dict[str, dict[str, Any]] = self.__Storage.open(file, {})
        default_prefixes: list[str] = [value.get("prefix", "") for value in prefixes.values()]

        if prefix in default_prefixes:
            return True

        prefix_uuid: str = None
        while not prefix_uuid or prefix_uuid in prefixes:
            prefix_uuid: str = str(uuid.uuid4())

        prefixes[prefix_uuid] = {
            "created_by":   created_by,
            "create_at":    create_at,
            "prefix":       prefix,
            "active":       active
        }

        return self.__Storage.save(prefixes, file)
    def client_add_prefix(self, prefix: str, create_at: str = str(datetime.now()), created_by: str = "None", active: bool = True) -> bool:
        return self.__add_prefix("client-prefixes.slze", prefix, create_at, created_by, active)
    def guild_add_prefix(self, id: str, prefix: str, create_at: str = str(datetime.now()), created_by: str = "None", active: bool = True) -> bool:
        return self.__add_prefix(f"Guilds/{id}.slze", prefix, create_at, created_by, active)
    def user_add_prefix(self, id: str, prefix: str, create_at: str = str(datetime.now()), created_by: str = "None", active: bool = True) -> bool:
        return self.__add_prefix(f"Users/{id}.slze", prefix, create_at, created_by, active)

    # ---------- Get ----------

    def __get_prefix(self, file: str) -> list[str]:
        prefixes: dict[str, dict[str, Any]] = self.__Storage.open(file, {})
        result: list[str] = []

        for value in prefixes.values():
            if value.get("active", False) and value.get("prefix", False):
                result.append(value.get("prefix"))

        return result
    def client_get_prefix(self) -> list[str]:
        return self.__get_prefix("client-prefixes.slze")
    def guild_get_prefix(self, id: str) -> list[str]:
        return self.__get_prefix(f"Guilds/{id}.slze")
    def user_get_prefix(self, id: str) -> list[str]:
        return self.__get_prefix(f"Users/{id}.slze")

    # ---------- Del ----------

    def __del_prefix(self, file: str, prefix: str) -> bool:
        prefixes: dict[str, dict[str, Any]] = self.__Storage.open(file, {})
        default_prefixes: list[str] = [value.get("prefix", "") for value in prefixes.values()]

        if prefix not in default_prefixes:
            return True

        for key, value in (prefixes.copy()).items():
            if value.get("prefix", "") == prefix:
                del prefixes[key]

        return self.__Storage.save(prefixes, file)
    def client_del_prefix(self, prefix: str) -> bool:
        return self.__del_prefix("client-prefixes.slze", prefix)
    def guild_del_prefix(self, id: str, prefix: str) -> bool:
        return self.__del_prefix(f"Guilds/{id}.slze", prefix)
    def user_del_prefix(self, id: str, prefix: str) -> bool:
        return self.__del_prefix(f"Users/{id}.slze", prefix)

    # ---------- enable ----------

    def __enable_prefix(self, file: str, prefix: str) -> bool:
        prefixes: dict[str, dict[str, Any]] = self.__Storage.open(file, {})
        default_prefixes: list[str] = [value.get("prefix", "") for value in prefixes.values()]

        if prefix not in default_prefixes:
            return False

        for key, value in (prefixes.copy()).items():
            if value.get("prefix", "") == prefix:
                prefixes[key]["active"] = True

        return self.__Storage.save(prefixes, file)
    def client_enable_prefix(self, prefix: str) -> bool:
        return self.__enable_prefix("client-prefixes.slze", prefix)
    def guild_enable_prefix(self, id: str, prefix: str) -> bool:
        return self.__enable_prefix(f"Guilds/{id}.slze", prefix)
    def user_enable_prefix(self, id: str, prefix: str) -> bool:
        return self.__enable_prefix(f"Users/{id}.slze", prefix)

    # ---------- disable ----------

    def __disable_prefix(self, file: str, prefix: str) -> bool:
        prefixes: dict[str, dict[str, Any]] = self.__Storage.open(file, {})
        default_prefixes: list[str] = [value.get("prefix", "") for value in prefixes.values()]

        if prefix not in default_prefixes:
            return False

        for key, value in (prefixes.copy()).items():
            if value.get("prefix", "") == prefix:
                prefixes[key]["active"] = False

        return self.__Storage.save(prefixes, file)
    def client_disable_prefix(self, prefix: str) -> bool:
        return self.__disable_prefix("client-prefixes.slze", prefix)
    def guild_disable_prefix(self, id: str, prefix: str) -> bool:
        return self.__disable_prefix(f"Guilds/{id}.slze", prefix)
    def user_disable_prefix(self, id: str, prefix: str) -> bool:
        return self.__disable_prefix(f"Users/{id}.slze", prefix)

    async def run(self, Client: commands.Bot, Message: discord.Message) -> list[str]:
        Result: list[str] = []

        Result.extend(self.client_get_prefix())

        if Message.guild and Message.guild.id:
            Result.extend(self.guild_get_prefix(Message.guild.id))

        if Message.author and Message.author.id:
            Result.extend(self.user_get_prefix(Message.author.id))

        return Result

# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.0y
