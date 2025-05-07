from discord.ext    import commands

from Slazhe.Discord import Cog, command, Context

class Ping(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @command(name="ping", description="Vérifie la latence")
    async def ping(self, ctx: Context):
        latency = round(self.bot.latency * 1000)
        
        await ctx.send(f"Pong! {latency}ms", reference=ctx.ctx.message)

async def setup(bot):
    return bot.add_cog(Ping(bot.bot))
# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.01
