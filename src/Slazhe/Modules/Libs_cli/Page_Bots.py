from Slazhe import Logger

Log = Logger(__package__)

from .BaseCliModule import SlazheCliModule, get_pm
from .Question      import Page, PageManager, QuestionPage

from rich.table import Table

from typing import Any

from Slazhe.Modules import importer

if hasattr(importer, "PermissionManager"):
    from Slazhe.Modules.Account import LoginManager 

if hasattr(importer, "BotManager"):
    from Slazhe.Modules.Libs_Bots.Bot_Manager import BotManager

class SlazheBots(SlazheCliModule):
    def _get_user_and_bots(self) -> tuple[Any, dict[str, Any]]:
        if not self.__User_Token or not self.__Login_Manager:
            raise ValueError("Missing user token or login manager")

        user = self.__Login_Manager.get_account_from_token(self.__User_Token)
        return user, user.bots

    def _create_page_manager(self, pages: list) -> PageManager:
        return PageManager(pages, console=self.console, prompt=self.prompt)

    def _create_bot_table(self, bots: list) -> Table:
        table = Table(title="Vos Bots", width=int(self.console.width / 2), title_style="")
        table.add_column("uuid", style="cyan")
        
        for bot in bots:
            table.add_column(bot.uuid, style="magenta")
        
        for attr in ["name", "id", "uuid", "intents_enable", "started", "is_ready"]:
            table.add_row(attr, *[str(getattr(bot, attr, "Unknown")) for bot in bots])
        
        return table

    def run(self) -> None:
        self.__User_Token: str              = self.opts.get("user_token")
        self.__Login_Manager: LoginManager  = self.opts.get("login_manager")

        if not self.__User_Token or not self.__Login_Manager:
            return

        self.Bot_Manager: BotManager = importer.BotManager()
        self.quit_main_loop: bool = False

        main_pages = [
            Page("Menu", 1, lambda: setattr(self, 'quit_main_loop', True)),
            Page("Liste complète des bots", 2, self.view_bots),
            Page("Gestion d'un bot", 3, self.gest_bot, [
                QuestionPage("UUID du bot", "uuid")
            ]),
            Page("Gestion des bots", 4),
            Page("Ajouter un bot", 5, self.add_bot, [
                QuestionPage("Token du bot", "token", password = True),
                QuestionPage("Nom du bot ( modifier lors du démarage du bot )", "name"),
                QuestionPage("Id du bot ( modifier lors du démarage du bot )", "id")
            ]),
            Page("Supprimer un bot", 6, self.del_bot, [
                QuestionPage("UUID du bot", "uuid")
            ])
        ]

        Page_Manager = self._create_page_manager(main_pages)

        while not self.quit_main_loop:
            Page_Manager.run()

    def view_bots(self) -> None:
        _, user_bots = self._get_user_and_bots()
        bots = [self.Bot_Manager.get_bot(uuid) for uuid in user_bots.keys()]
        bots = [b for b in bots if b]
        
        if not bots:
            Log.Info("Aucun bot trouvé")
            return

        self.console.print(self._create_bot_table(bots), justify="center")

    def _create_bot_management_pages(self, uuid: str) -> list:
        return [
            Page("retours", 1, lambda: setattr(self, 'quit_gest_loop', True)),
            Page("Configurer le bot", 2, self.conf_gest_bot, attrs={"uuid": uuid}),
            Page("Démarrer le bot", 3, lambda: self.Bot_Manager.start_bot(uuid)),
            Page("Arrêter le bot", 4, lambda: self.Bot_Manager.stop_bot(uuid))
        ]

    def gest_bot(self, uuid: str) -> None:
        _, user_bots = self._get_user_and_bots()
        if uuid not in user_bots or not self.Bot_Manager.get_bot(uuid):
            return Log.Warn("Ce bot n'existe pas !")
        
        self.quit_gest_loop = False
        Page_Manager = self._create_page_manager(self._create_bot_management_pages(uuid))
        
        while not self.quit_gest_loop:
            Page_Manager.run()

    def _create_config_pages(self, uuid: str) -> list:
        """Helper to create configuration pages."""
        return [
            Page("retours", 1, lambda: setattr(self, 'quit_conf_gest_loop', True)),
            Page("Démarage au lancement", 2, 
                lambda choice: self.Bot_Manager.start_at_boot(
                    uuid, choice.lower() == "oui"
                ), [
                    QuestionPage("Démarage au lancement ?", "choice", 
                               choices=["oui", "non"], case_sensitive=False)
                ]),
        ]

    def conf_gest_bot(self, uuid: str) -> None:
        _, user_bots = self._get_user_and_bots()
        if uuid not in user_bots or not self.Bot_Manager.get_bot(uuid):
            return Log.Warn("Ce bot n'existe pas !")
        
        self.quit_conf_gest_loop = False
        Page_Manager = self._create_page_manager(self._create_config_pages(uuid))

        while not self.quit_conf_gest_loop:
            Page_Manager.run()

    def add_bot(self, token: str, name: str, id: str) -> None:
        uuid = self.Bot_Manager.add_bot(token, name, id, False)

        user, user_bots = self._get_user_and_bots()
        user_bots[uuid] = {}

        user.bots = user_bots

    def del_bot(self, uuid: str) -> None:
        user, user_bots = self._get_user_and_bots()
        if uuid not in user_bots or not self.Bot_Manager.get_bot(uuid):
            return Log.Warn("Ce bot n'existe pas !")

        self.Bot_Manager.del_bot(uuid)

        new_user_bots = user_bots.copy()
        del new_user_bots[uuid]
        user.bots = new_user_bots

        Log.Info(f"Le bot {uuid} est supprimée.")

# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.10
