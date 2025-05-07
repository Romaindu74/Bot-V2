from Slazhe import Logger

Log = Logger(__name__)

from Slazhe.Modules import importer

if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

import json

from typing         import Any, Optional
from .account       import Account

import hashlib
import secrets
from datetime import datetime, timedelta

def OpenStorage(data: str) -> dict:
    try:
        return json.loads(data)
    except Exception as e:
        print(e)
        return {}

def SaveStorage(data: dict) -> str:
    return json.dumps(data)

class Session:
    def __init__(self, account: Account, duration_minutes: int = 30, **attrs):
        self.__account      = account
        self.__expires_at   = datetime.now() + timedelta(minutes=duration_minutes)
        self.__token        = secrets.token_hex(32)
        self.attrs: dict[Any] = attrs

    @property
    def token(self) -> str:
        return self.__token

    @property
    def account(self) -> Optional[Account]:
        if self.is_active():
            return self.__account
    
        return None

    @property
    def account_for_save(self) -> Account:
        return self.__account

    def is_active(self) -> bool:
        return datetime.now() < self.__expires_at

class SessionLogOut:
    def __getattr__(self, name: str) -> Any:
        raise Exception("Tu est déconnecter.")

class LoginManager:
    def __init__(self) -> None:
        if not hasattr(importer, "Storage") or importer.Storage is None:
            raise ValueError("Storage is not available.")

        self.__Storage: TypingStorage = importer.Storage("var/slazhe-users", __file__, SaveStorage, OpenStorage, True)
        self.__sessions_by_token: dict[str, Session] = {}

    def __hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> str:
        Users: dict[str, Any] = self.__Storage.open("users.slze", {})
        User:  dict[str, Any] = Users.get(username, None)

        if User is None:
            raise ValueError("Utilisateur introuvable")

        if self.__hash_password(password) != User.get("password_hash", None):
            raise ValueError("Mot de passe incorrect")

        account = Account(User["uuid"], self.__hash_password(password))
        session = Session(account, username = username)
        self.__sessions_by_token[session.token] = session

        return session.token

    def logout(self, token: str) -> None:
        if not token in self.__sessions_by_token:
            return
        
        Session = self.__sessions_by_token.get(token)
        account = Session.account_for_save

        Users: dict[str, Any] = self.__Storage.open("users.slze", {})
        User: dict[str, Any]  = Users.get(Session.attrs.get("username", None), None)

        if Session.attrs.get("username", None) != account.username:
            Users[account.username] = User.copy()

            del Users[Session.attrs.get("username", None)]

            self.__Storage.save(Users, "users.slze")

        if account.hash_password != Users[account.username].get("password_hash", None):
            Users[account.username]["password_hash"] = account.hash_password

            self.__Storage.save(Users, "users.slze")

        account.save()
        account.close()

        del self.__sessions_by_token[token]

    def get_account_from_token(self, token: str) -> Optional[Account]:
        session = self.__sessions_by_token.get(token)
        if session and session.is_active():
            return session.account
        
        self.logout(token)

        return None
# Version Globale: v00.00.00.pl
# Version du fichier: v00.00.00.1c
