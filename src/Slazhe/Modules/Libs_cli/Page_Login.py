from Slazhe import Logger

Log = Logger(__package__)

from .BaseCliModule import SlazheCliModule, get_pm
from .Question      import Page, PageManager, QuestionPage

from .Page_ShowModules  import CliShowModules
from .Page_Bots         import SlazheBots

from rich.table import Table

from typing import Any

from Slazhe.Modules import importer

if hasattr(importer, "PermissionManager"):
    from Slazhe.Modules.Account import LoginManager

class SlazheLogin(SlazheCliModule):
    """
    CLI module for user login.
    """

    def run(self, username: str, password: str) -> None:
        self.__Login_Manager = LoginManager()

        self.__UserToken: str = self.__Login_Manager.login(username, password)
        if self.__UserToken is None:
            return self.console.print("[red]Connexion échouée[/red]")

        self.quit = False

        def menu():
            self.__Login_Manager.logout(self.__UserToken)
            self.__Login_Manager = self.__UserToken = None
            self.quit = True

        pages = [
            Page("Se Déconnecter", 1, menu),
            Page("Mon Profile", 2, self.profile),
            Page("Mes Bots", 3, SlazheBots, attrs={ "parent": self, "user_token": self.__UserToken, "login_manager": self.__Login_Manager }),
            Page("Page Admin", 4),
            Page("Modules chargés", 5, CliShowModules, attrs={ "parent": self })
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt, title=f"Bonjour {username}")

        while not self.quit:
            page_manager.run()

    def profile(self) -> None:
        self.quit_profile = False

        def profile_quit():
            self.quit_profile = True

        def profile_print():
            Profile_Table = Table(title = "Votre profile", width=int(self.console.width / 2), title_style="")
            Profile_Table.add_column("Name", style="cyan")
            Profile_Table.add_column("Value", style="magenta")

            UserAccount = self.__Login_Manager.get_account_from_token(self.__UserToken)

            if UserAccount is None:
                Log.Error("Vous êtes déconnecter, veuillez vous reconnecter.")
                self.quit = self.quit_profile = True

                return

            for Element in dir(UserAccount):
                if Element not in ["bots_length", "created_at", "updated_at", "email", "id", "username", "uuid"]:
                    continue

                Profile_Table.add_row(Element, str(getattr(UserAccount, Element)))

            self.console.print(Profile_Table, justify="center")

        pages = [
            Page("Menu", 1, profile_quit),
            Page("Voir mon profile", 2, profile_print),
            Page("Modifier mon profile", 3, self.edit_profile)
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt)

        while not self.quit_profile:
            page_manager.run()

    def edit_profile(self) -> None:
        self.quit_edit_profile = False

        def edit_quit():
            self.quit_edit_profile = True

        UserAccount = self.__Login_Manager.get_account_from_token(self.__UserToken)

        if UserAccount is None:
            Log.Error("Vous êtes déconnecter, veuillez vous reconnecter.")
            self.quit = self.quit_profile = True

            return

        pages = [
            Page("Retours", 1, edit_quit),
            Page("Modifier mon Nom", 2, UserAccount._edit_profile_info, [ QuestionPage("Nouveau Nom", "value", console=self.console, prompt=self.prompt) ], attrs={ "element": "username" }),
            Page("Modifier mon Mot de passe", 3, UserAccount._edit_password, [
                QuestionPage("Mot de passe", "password", console=self.console, prompt=self.prompt, password = True),
                QuestionPage("Nouveau mot de passe", "new_password", console=self.console, prompt=self.prompt, password = True),
                QuestionPage("Réecriver votre nouveau mot de passe", "new2_password", console=self.console, prompt=self.prompt, password = True)
            ]),
            Page("Modifier mon E-mail", 4, UserAccount._edit_profile_info, [ QuestionPage("Nouvelle E-mail", "value", console=self.console, prompt=self.prompt) ], attrs={ "element": "email" })
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt)

        while not self.quit_edit_profile:
            page_manager.run()
# Version Globale: v00.00.00.pl
# Version du fichier: v00.00.00.13
