from Slazhe import Logger
from Slazhe.Modules import importer
from typing import Any, Dict
import json, datetime
from .permission import PermissionManager

Log = Logger(__name__)

if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

class Account:
    USER_STORAGE_PATH = "users-data/{user_uuid}.slze"
    STORAGE_ROOT = "var/slazhe-users"

    def __init__(self, user_uuid: str, password: str) -> None:
        """Initialize an Account instance.
        
        Args:
            user_uuid: The unique identifier for the user
            password: The hashed password (must be hashed)
        
        Raises:
            ValueError: If Storage is not available
        """
        if not hasattr(importer, "Storage") or importer.Storage is None:
            raise ValueError("Storage is not available.")

        self.__user_storage_path = self.USER_STORAGE_PATH.format(user_uuid=user_uuid)
        self.__user_uuid = user_uuid
        self.__user_pass = password

        self.__Storage: TypingStorage = importer.Storage(
            self.STORAGE_ROOT, 
            __file__, 
            self._save_storage, 
            self._open_storage
        )
        self.__user_data: Dict[str, Any] = self.__Storage.open(
            self.__user_storage_path, 
            {}, 
            password
        )
        self.__permission = PermissionManager(user_uuid, password)

    @staticmethod
    def _open_storage(data: str) -> Dict[str, Any]:
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
    def _save_storage(data: Dict[str, Any]) -> str:
        """Helper method to save storage data."""
        return json.dumps(data)

    def save(self) -> None:
        """Save the user data to storage."""
        self.__permission.save(self.__user_pass)
        self.__Storage.save(self.__user_data, self.__user_storage_path, self.__user_pass)

    def close(self) -> None:
        """Close the account (no operation needed currently)."""
        self.__user_storage_path = self.__user_pass = self.__user_uuid = self.__user_data = self.__Storage = None

    @property
    def username(self) -> str:
        """Get the username."""
        return self.__user_data.get("name", "Unknown")
    
    @username.setter
    def username(self, value: str) -> None:
        """Set the username."""
        self.__user_data["name"] = value

    @property
    def uuid(self) -> str:
        """Get the user UUID."""
        return self.__user_uuid
    
    @property
    def force_reset_password(self) -> bool:
        """Check if password reset is required."""
        return self.__user_data.get("reset_password", False)

    def has_permission(self, permission_id: str) -> bool:
        """Check if user has specified permission."""
        return self.__permission.has_permission(permission_id)
    
    @property
    def id(self) -> str:
        """Get user ID (placeholder implementation)."""
        return self.__user_data.get("id", "Unknown")

    @property
    def email(self) -> str:
        """Get user email (placeholder implementation)."""
        return self.__user_data.get("email", "Unknown")

    @email.setter
    def email(self, value: str) -> None:
        """Set the email."""
        self.__user_data["email"] = value

    @property
    def created_at(self) -> str:
        """Get creation date (placeholder implementation)."""
        return self.__user_data.get("created_at", datetime.datetime.now())

    @property
    def updated_at(self) -> str:
        """Get last update date (placeholder implementation)."""
        return self.__user_data.get("updated_at", datetime.datetime.now())

    @property
    def preferences(self) -> Dict[str, Any]:
        """Get user preferences (placeholder implementation)."""
        return {}

    @property
    def bots_length(self) -> int:
        """Get number of bots (placeholder implementation)."""
        return len(self.bots.keys())

    @property
    def bots(self) -> dict[str, Any]:
        return self.__user_data.get("bots", {})
    
    @bots.setter
    def bots(self, value: dict[str, Any]) -> None:
        self.__user_data["bots"] = value

    @property
    def hash_password(self) -> str:
        return self.__user_pass

    def _edit_profile_info(self, element: str, value: str) -> None:
        """Edit profile information.
        
        Args:
            element: The attribute to modify
            value: The new value
            
        Note:
            Won't modify protected attributes (uuid, id)
        """
        if not hasattr(self, element) or element in ("uuid", "id"):
            return Log.Error(f"Unknown or protected attribute: {element}")

        if value == "":
            return Log.Error("La valeur ne peux pas être vide.")

        self.__user_data["update_at"] = str(datetime.datetime.now())

        Log.Info("Changement effectuer.")

        setattr(self, element, value)

    def _edit_password(self, password: str, new_password: str, new2_password: str) -> None:
        if new_password != new2_password:
            return Log.Error("Les mot de passe ne correspond pas.")
        
        import hashlib

        hash_password: str = hashlib.sha256(password.encode()).hexdigest()

        if self.__user_pass != hash_password:
            return Log.Error("Mot de passe invalid.")
        
        new_hash_password: str = hashlib.sha256(new_password.encode()).hexdigest()

        self.__user_pass = new_hash_password
        self.save()

        Log.Info("Mot de passe changer.")
# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.19
