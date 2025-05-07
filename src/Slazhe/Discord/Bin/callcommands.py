from discord.ext import commands
from .command import Command
from .context import Context
import discord

from typing import Any

class callcommands:
    def __init__(self):
        self.__commands: dict[str, Command] = {}

    def decorator(self, Bot: commands.Bot, command: Command) -> None:
        @Bot.tree.command(**command.info)
        async def decorator_app(ctx: discord.Interaction) -> None:
            __new_ctx = Context(ctx, command, Bot)
            await __new_ctx.get_context()

            if command.typing:
                await __new_ctx.typing(ephemeral = command.ephemeral)

            params: dict[str, Any] = await __new_ctx.from_data()

            await command(__new_ctx, **params)

        @Bot.command(**command.info)
        async def decorator_bot(ctx: commands.Context, *args, **kwargs) -> None:
            if (ctx.guild and ctx.guild.id and command.guild_ids) and ctx.guild.id not in command.guild_ids:
                return

            try:
                if command.typing:
                    await ctx.typing(ephemeral = command.ephemeral)

                __new_ctx: Context = Context(ctx, command, Bot, *args, **kwargs)

                params: dict[str, Any] = await __new_ctx.from_data()

                await command(__new_ctx, **params)
            except Exception as e:
                print(e)
# Version Globale: v00.00.00.ol
# Version du fichier: v00.00.00.0n
