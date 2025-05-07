from Slazhe import Logger

Log = Logger(__name__)

from Slazhe.Modules import importer

if getattr(importer, 'Storage', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

import string
import random

def gen_string(length: int = 8) -> str:
    chars: str = string.digits + string.ascii_letters
    result: str = ""

    for i in range(length):
        result += chars[int(random.random() * (len(chars) - 1))]

    return result

from typing import Dict, Any

import json
import hashlib
import uuid

from datetime import datetime

All_Permissions: dict[str, dict[str, str]] = {
    "1": {"name": "dashboard", "description": "Accéder au tableau de bord."},
    "2": {"name": "use_bots", "description": "Utiliser les bots."},
    "3": {"name": "view_logs", "description": "Voir les journaux d'activité."},
    "4": {"name": "manage_own_bots", "description": "Gérer ses propres bots."},
    "5": {"name": "create_own_bots", "description": "Créer ses propres bots."},
    "6": {"name": "delete_own_bots", "description": "Supprimer ses propres bots."},
    "7": {"name": "start_own_bots", "description": "Démarrer ses propres bots."},
    "8": {"name": "stop_own_bots", "description": "Arrêter ses propres bots."},
    "9": {"name": "edit_own_bots", "description": "Modifier ses propres bots."},
    "10": {"name": "view_own_bot_config", "description": "Voir la configuration de ses propres bots."},
    "11": {"name": "manage_all_bots", "description": "Gérer tous les bots."},
    "12": {"name": "create_all_bots", "description": "Créer tous les bots."},
    "13": {"name": "delete_all_bots", "description": "Supprimer tous les bots."},
    "14": {"name": "start_all_bots", "description": "Démarrer tous les bots."},
    "15": {"name": "stop_all_bots", "description": "Arrêter tous les bots."},
    "16": {"name": "edit_all_bots", "description": "Modifier tous les bots."},
    "17": {"name": "view_all_bot_config", "description": "Voir la configuration de tous les bots."},
    "18": {"name": "manage_users", "description": "Gérer les utilisateurs."},
    "19": {"name": "create_users", "description": "Créer des utilisateurs."},
    "20": {"name": "delete_users", "description": "Supprimer des utilisateurs."},
    "21": {"name": "edit_users", "description": "Modifier des utilisateurs."},
    "22": {"name": "view_user_logs", "description": "Voir les journaux des utilisateurs."},
    "23": {"name": "assign_roles", "description": "Attribuer des rôles."},
    "24": {"name": "manage_roles", "description": "Gérer les rôles."},
    "25": {"name": "manage_modules", "description": "Gérer les modules."},
    "26": {"name": "develop_modules", "description": "Développer des modules."},
    "27": {"name": "deploy_modules", "description": "Déployer des modules."},
    "28": {"name": "audit_access", "description": "Auditer l'accès."},
    "29": {"name": "generate_reports", "description": "Générer des rapports."},
    "30": {"name": "view_reports", "description": "Voir les rapports."},
    "31": {"name": "configure_settings", "description": "Configurer les paramètres."},
    "32": {"name": "super_admin", "description": "Accès super administrateur."},
    "33": {"name": "clone_own_bots", "description": "Cloner ses propres bots."},
    "34": {"name": "clone_all_bots", "description": "Cloner tous les bots."},
    "35": {"name": "schedule_own_bots", "description": "Planifier ses propres bots."},
    "36": {"name": "schedule_all_bots", "description": "Planifier tous les bots."},
    "37": {"name": "export_own_bot_data", "description": "Exporter les données de ses propres bots."},
    "38": {"name": "export_all_bot_data", "description": "Exporter les données de tous les bots."},
    "39": {"name": "import_bots", "description": "Importer des bots."},
    "40": {"name": "analyze_own_bots", "description": "Analyser ses propres bots."},
    "41": {"name": "analyze_all_bots", "description": "Analyser tous les bots."},
    "42": {"name": "assign_bots_to_users", "description": "Attribuer des bots aux utilisateurs."},
    "43": {"name": "tag_bots", "description": "Tagger les bots."},
    "44": {"name": "view_bot_history", "description": "Voir l'historique des bots."},
    "45": {"name": "rollback_bot_version", "description": "Restaurer une version précédente d'un bot."},
    "46": {"name": "root_permissions", "description": "Permissions racine."},
    "47": {"name": "assign_permission", "description": "Pour ajouter une permission à quelqu’un."},
    "48": {"name": "delete_permission", "description": "Pour retirer une permission."},
    "49": {"name": "create_permission", "description": "Pour ajouter une nouvelle permission."}
}

def _save_storage(data: Dict[str, Any]) -> str:
    return json.dumps(data)

def root_account():
    if not hasattr(importer, "Storage") or importer.Storage is None:
        raise ValueError("Storage is not available.")

    root_password: str      = gen_string(10)
    root_password_hash: str = hashlib.sha256(root_password.encode()).hexdigest()
    root_uuid: str          = str(uuid.uuid4())

    path: str = "var/slazhe-users"

    UserStorage: TypingStorage = importer.Storage(path, "login.py", _save_storage, encrypt = False)
    UserStorage.save({
        "root": { "password_hash": root_password_hash, "uuid": root_uuid }
    }, "users.slze")

    AccountStorage: TypingStorage = importer.Storage(path, "account.py", _save_storage, encrypt = False)
    AccountStorage.save({
        "name": "root",
        "id": "0",
        "email": "romain@slazhe.com",
        "uuid": root_uuid,
        "created_at": str(datetime.now())
    }, f"users-data/{root_uuid}.slze", root_password_hash)

    Log.Info("Le mot de passe root est: ", root_password)

    Permissions: TypingStorage = importer.Storage(path, "permission.py", _save_storage, encrypt = False)
    Permissions.save(All_Permissions, "permission.slze")
    Permissions.save({"permission": list(All_Permissions.keys())}, f"users-permission/{root_uuid}.slze", root_password_hash)
# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.0o
