from Slazhe import Logger

Log = Logger(__name__)

import uuid
from typing import Any, Callable
from .Libs.listeners import AllListeners
from asyncio import iscoroutinefunction

class Listeners:
    def __init__(self, Client: Any):
        self.__client: Any = Client

        self.__event_listeners = AllListeners(self.__on_event)
        self.__listeners: dict[str, dict[str, Callable[[Any], None]]] = {}

    async def bot_add_cog(self) -> bool:
        try:
            await self.__client.bot.add_cog(self.__event_listeners)
        except Exception:
            return False
        else:
            return True


    def add_event_listener(self, event: str, callback: Callable[[Any], None]) -> str:
        event_uuid = str(uuid.uuid4())

        if event in self.__listeners:
            self.__listeners[event][event_uuid] = callback

        else:
            self.__listeners[event] = { event_uuid : callback }

        return event_uuid

    def del_event_listener(self, event: str, uuid: str) -> None:
        if event not in self.__listeners:
            return
        
        if uuid not in self.__listeners[event]:
            return
        
        del self.__listeners[event][uuid]

        if self.__listeners[event] == {}:
            del self.__listeners[event]

    async def __on_event(self, event: str, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        if event not in self.__listeners:
            return
        
        for callback in (self.__listeners.copy())[event].values():
            try:
                if iscoroutinefunction(callback):
                    await callback(*args, **kwargs)
                else:
                    callback(self.__client, *args, **kwargs)    
            except Exception as e:
                print(f"Error in {event} listener: {e}")
# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.08
