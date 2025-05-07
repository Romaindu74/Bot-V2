from Slazhe import Logger

Log = Logger(__name__)

from Slazhe.Modules import importer

if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

from .Bots import SlazheBot

from typing import Self, Any, Dict, Optional
import json, uuid, os
import shutil


class BotManager:
    __instance: Self = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__Storage: TypingStorage = importer.Storage(f"var/Slazhe-Bots/", __file__,
                cls.__save_storage,
                cls.__open_storage,
                True
                )
            cls.__bots: dict[str, SlazheBot] = {}

        return cls.__instance

    def check(self) -> None:
        bots: dict[str, dict[str, bool]] = self.__Storage.open('managers.slze', {})

        for bot, value in bots.items():
            if bot in self.__bots:
                continue

            try:
                self.__bots[bot] = SlazheBot(bot)
            except ValueError:
                continue

            else:
                if value.get("start-at-boot", False):
                    self.__bots[bot].start()

    @property
    def get_bots(self) -> dict[str, SlazheBot]:
        return self.__bots
    
    def get_bot(self, uuid: str) -> Optional[SlazheBot]:
        return self.__bots.get(uuid, None)

    def start_bot(self, uuid: str) -> None:
        Bot = self.get_bot(uuid)

        if Bot is None or Bot.started:
            return
        
        Bot.start()

    def stop_bot(self, uuid: str) -> None:
        Bot = self.get_bot(uuid)

        if Bot is None or not Bot.started:
            return
        
        Bot.stop()

    def add_bot(self, token: str, name: Optional[str] = None, id: Optional[str] = None, start_at_boot: bool = False) -> str:
        bot_uuid = str(uuid.uuid4())
        while bot_uuid in self.__bots:
            bot_uuid = str(uuid.uuid4())

        bot_storage: TypingStorage = importer.Storage(
            f"var/Slazhe-Bots/{bot_uuid}/", bot_uuid,
            self.__save_storage, self.__open_storage
        )

        bot_storage.save({
            "token": token,
            "name":  name or "Unnamed Bot",
            "id":    id or "Unknown"
        }, "main.slze")

        bots = self.__Storage.open('managers.slze', {})
        bots[bot_uuid] = {"start-at-boot": start_at_boot}
        self.__Storage.save(bots, 'managers.slze')

        self.__bots[bot_uuid] = SlazheBot(bot_uuid)

        if start_at_boot:
            self.__bots[bot_uuid].start()

        return bot_uuid

    def del_bot(self, uuid: str) -> None:
        if uuid not in self.__bots and uuid not in self.__Storage.open('managers.slze', {}):
            Log.Warn(f"Bot {uuid} not found for deletion")
            return
        
        if uuid in self.__bots:
            Bot: SlazheBot = self.__bots[uuid]
            if Bot.started:
                Bot.stop()

            del self.__bots[uuid]

        Bots: dict[str, Any] = self.__Storage.open('managers.slze', {})
        if uuid in Bots:
            del Bots[uuid]

            self.__Storage.save(Bots, 'managers.slze')

        path_bot: str = f"var/Slazhe-Bots/{uuid}/"
        if importer.Storage.exists(path_bot):
            shutil.rmtree(path_bot)

    def start_at_boot(self, uuid: str, start: bool = False) -> None:
        bots: dict[str, dict[str, bool]] = self.__Storage.open('managers.slze', {})

        if not bots.get(uuid, False):
            return
        
        bots[uuid] = { "start-at-boot": start }

        self.__Storage.save(bots, 'managers.slze')

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

# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.0t
