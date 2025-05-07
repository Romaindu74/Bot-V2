from discord.ext    import commands

from Slazhe.Discord import Cog, command, Context

import discord
from discord.ui import Button, View

class MyView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Pas de timeout, le bouton reste actif

    @discord.ui.button(label="Commande 1", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Tu as cliqué sur Commande 1 !", ephemeral=True)

    @discord.ui.button(label="Commande 2", style=discord.ButtonStyle.success)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Tu as cliqué sur Commande 2 !", ephemeral=True)


class Help(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.bot.remove_command("help")

    @command(name="help", description="Cela peut vous aidée")
    async def help(self, ctx: Context):
        await ctx.send(f"Help is not set", reference=ctx.ctx.message, view=MyView())

async def setup(bot):
    return bot.add_cog(Help(bot.bot))
# Version Globale: v00.00.00.pl
# Version du fichier: v00.00.00.01
