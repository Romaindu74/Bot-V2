from discord.ext.commands   import Context as ContextT
from discord                import Interaction as InteractionT

from .utils import _BaseCommand

from typing import Union, Any, Optional, Sequence, overload
from discord import *
from discord.ui import View
from discord.context_managers import *
from discord.ext.commands.context import DeferTyping
from discord.utils import *

from discord import AppCommandOptionType

option_type_to_class = {
    AppCommandOptionType.string:        str,    # 3 - Chaîne de caractères
    AppCommandOptionType.integer:       int,    # 4 - Nombre entier
    AppCommandOptionType.boolean:       bool,   # 5 - Booléen
    AppCommandOptionType.user:          User,   # 6 - Utilisateur/Membre
    AppCommandOptionType.channel:       abc.GuildChannel,  # 7 - Salon (textuel, vocal, catégorie)
    AppCommandOptionType.role:          Role,   # 8 - Rôle
    AppCommandOptionType.mentionable:   Union[User, Role],  # 9 - Mentionable (user ou rôle)
    AppCommandOptionType.number:        float,  # 10 - Nombre décimal
    AppCommandOptionType.attachment:    Attachment,  # 11 - Fichier joint
}
from typing import Union
from discord import AppCommandOptionType, User, Role, Attachment
from discord.abc import GuildChannel

option_type_to_class = {
    AppCommandOptionType.string:        str,    # 3 - Chaîne de caractères
    AppCommandOptionType.integer:       int,    # 4 - Nombre entier
    AppCommandOptionType.boolean:       bool,   # 5 - Booléen
    AppCommandOptionType.user:          User,   # 6 - Utilisateur/Membre
    AppCommandOptionType.channel:       GuildChannel,  # 7 - Salon (textuel, vocal, catégorie)
    AppCommandOptionType.role:          Role,   # 8 - Rôle
    AppCommandOptionType.mentionable:   Union[User, Role],  # 9 - Mentionable (user ou rôle)
    AppCommandOptionType.number:        float,  # 10 - Nombre décimal
    AppCommandOptionType.attachment:    Attachment,  # 11 - Fichier joint
}

def get_arg_type(argument: str) -> AppCommandOptionType:
    if not isinstance(argument, str):
        raise TypeError("Argument must be a string")
    
    if argument.startswith('<@&'):
        return AppCommandOptionType.role
    elif argument.startswith('<@') and not argument.startswith('<@&'):
        return AppCommandOptionType.user  # Plus précis que mentionable
    elif argument.startswith('<#'):
        return AppCommandOptionType.channel
    
    # Vérification des nombres
    try:
        if '.' in argument:
            float(argument)
            return AppCommandOptionType.number
        else:
            int(argument)
            return AppCommandOptionType.integer
    except ValueError:
        pass
    
    # Vérification des booléens
    if argument.lower() in ('true', 'false', 'vrai', 'faux', '1', '0'):
        return AppCommandOptionType.boolean
    
    # Par défaut, on considère que c'est une chaîne
    return AppCommandOptionType.string

class Context:
    def __init__(self, ctx: Union[InteractionT, ContextT], command: _BaseCommand, Bot: Any, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self.__default_ctx: Union[InteractionT, ContextT] = ctx
        self.__interaction: bool = isinstance(ctx, InteractionT)

        self.__ctx: ContextT            = None
        self.__args: tuple[Any]         = args
        self.__kwargs: dict[str, Any]   = kwargs

        self.__command: _BaseCommand    = command

    async def from_data(self) -> dict[str, Any]:
        if self.__interaction:
            options: list[dict[str, Any]] = self.__default_ctx.data.get('options', [])
        else:
            options: list[dict[str, Any]] = []

            params: list = self.__command._params.values()
            for index, param in enumerate(params, 1):
                if index > len(self.__args):
                    if param.required:
                        return await self.ctx.send("Il manque des arguments !")
                    break

                arg = self.__args[index - 1]

                typearg = get_arg_type(arg)

                if typearg != param.type and param.type != AppCommandOptionType.string:
                    return await self.ctx.send("Voici les paramètres !")
                
                options.append({
                    'name': param.name,
                    'value': arg,
                    'type': typearg
                })

        return {
            o.get('name'): o.get('value') for o in options
        }

    async def get_context(self) -> None:
        if self.__interaction and self.__ctx is None:
            self.__ctx = await ContextT.from_interaction(self.__default_ctx)

    @property
    def ctx(self) -> ContextT:
        if self.__interaction:
            return self.__ctx
        return self.__default_ctx
    
    @property
    def filesize_limit(self) -> int:
        """:class:`int`: Returns the maximum number of bytes files can have when uploaded to this guild or DM channel associated with this context.

        .. versionadded:: 2.3
        """
        return self.ctx.filesize_limit

    @property
    def guild(self) -> Optional[Guild]:
        """Optional[:class:`.Guild`]: Returns the guild associated with this context's command. None if not available."""
        return self.ctx.guild

    @property
    def channel(self) -> TextChannel:
        """Union[:class:`.abc.Messageable`]: Returns the channel associated with this context's command.
        Shorthand for :attr:`.Message.channel`.
        """
        return self.ctx.channel

    @property
    def author(self) -> Union[User, Member]:
        """Union[:class:`~discord.User`, :class:`.Member`]:
        Returns the author associated with this context's command. Shorthand for :attr:`.Message.author`
        """
        return self.author

    @property
    def me(self) -> Union[Member, ClientUser]:
        """Union[:class:`.Member`, :class:`.ClientUser`]:
        Similar to :attr:`.Guild.me` except it may return the :class:`.ClientUser` in private message contexts.
        """
        # bot.user will never be None at this point.
        return self.ctx.me

    @property
    def permissions(self) -> Permissions:
        """:class:`.Permissions`: Returns the resolved permissions for the invoking user in this channel.
        Shorthand for :meth:`.abc.GuildChannel.permissions_for` or :attr:`.Interaction.permissions`.

        .. versionadded:: 2.0
        """
        return self.ctx.permissions

    @property
    def bot_permissions(self) -> Permissions:
        """:class:`.Permissions`: Returns the resolved permissions for the bot in this channel.
        Shorthand for :meth:`.abc.GuildChannel.permissions_for` or :attr:`.Interaction.app_permissions`.

        For interaction-based commands, this will reflect the effective permissions
        for :class:`Context` calls, which may differ from calls through
        other :class:`.abc.Messageable` endpoints, like :attr:`channel`.

        Notably, sending messages, embedding links, and attaching files are always
        permitted, while reading messages might not be.

        .. versionadded:: 2.0
        """
        return property

    @property
    def voice_client(self) -> Optional[VoiceProtocol]:
        r"""Optional[:class:`.VoiceProtocol`]: A shortcut to :attr:`.Guild.voice_client`\, if applicable."""
        return self.ctx.voice_client

    @overload
    async def reply(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embed: Embed = ...,
        file: File = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    @overload
    async def reply(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embed: Embed = ...,
        files: Sequence[File] = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    @overload
    async def reply(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embeds: Sequence[Embed] = ...,
        file: File = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    @overload
    async def reply(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embeds: Sequence[Embed] = ...,
        files: Sequence[File] = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    async def reply(self, content: Optional[str] = None, **kwargs: Any) -> Message:
        """|coro|

        A shortcut method to :meth:`send` to reply to the
        :class:`~discord.Message` referenced by this context.

        For interaction based contexts, this is the same as :meth:`send`.

        .. versionadded:: 1.6

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` or
            :exc:`ValueError` instead of ``InvalidArgument``.

        Raises
        --------
        ~discord.HTTPException
            Sending the message failed.
        ~discord.Forbidden
            You do not have the proper permissions to send the message.
        ValueError
            The ``files`` list is not of the appropriate size
        TypeError
            You specified both ``file`` and ``files``.

        Returns
        ---------
        :class:`~discord.Message`
            The message that was sent.
        """
        return await self.ctx.reply(content, **kwargs)

    def typing(self, *, ephemeral: bool = False) -> Union[Typing, DeferTyping]:
        """Returns an asynchronous context manager that allows you to send a typing indicator to
        the destination for an indefinite period of time, or 10 seconds if the context manager
        is called using ``await``.

        In an interaction based context, this is equivalent to a :meth:`defer` call and
        does not do any typing calls.

        Example Usage: ::

            async with channel.typing():
                # simulate something heavy
                await asyncio.sleep(20)

            await channel.send('Done!')

        Example Usage: ::

            await channel.typing()
            # Do some computational magic for about 10 seconds
            await channel.send('Done!')

        .. versionchanged:: 2.0
            This no longer works with the ``with`` syntax, ``async with`` must be used instead.

        .. versionchanged:: 2.0
            Added functionality to ``await`` the context manager to send a typing indicator for 10 seconds.

        Parameters
        -----------
        ephemeral: :class:`bool`
            Indicates whether the deferred message will eventually be ephemeral.
            Only valid for interaction based contexts.

            .. versionadded:: 2.0
        """
        return self.ctx.typing(ephemeral = ephemeral)

    async def defer(self, *, ephemeral: bool = False) -> None:
        """|coro|

        Defers the interaction based contexts.

        This is typically used when the interaction is acknowledged
        and a secondary action will be done later.

        If this isn't an interaction based context then it does nothing.

        Parameters
        -----------
        ephemeral: :class:`bool`
            Indicates whether the deferred message will eventually be ephemeral.

        Raises
        -------
        HTTPException
            Deferring the interaction failed.
        InteractionResponded
            This interaction has already been responded to before.
        """

        return self.ctx.defer(ephemeral = ephemeral)

    @overload
    async def send(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embed: Embed = ...,
        file: File = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    @overload
    async def send(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embed: Embed = ...,
        files: Sequence[File] = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    @overload
    async def send(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embeds: Sequence[Embed] = ...,
        file: File = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    @overload
    async def send(
        self,
        content: Optional[str] = ...,
        *,
        tts: bool = ...,
        embeds: Sequence[Embed] = ...,
        files: Sequence[File] = ...,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = ...,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: AllowedMentions = ...,
        reference: Union[Message, MessageReference, PartialMessage] = ...,
        mention_author: bool = ...,
        view: View = ...,
        suppress_embeds: bool = ...,
        ephemeral: bool = ...,
        silent: bool = ...,
        poll: Poll = ...,
    ) -> Message:
        ...

    async def send(
        self,
        content: Optional[str] = None,
        *,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[Sequence[Embed]] = None,
        file: Optional[File] = None,
        files: Optional[Sequence[File]] = None,
        stickers: Optional[Sequence[Union[GuildSticker, StickerItem]]] = None,
        delete_after: Optional[float] = None,
        nonce: Optional[Union[str, int]] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        reference: Optional[Union[Message, MessageReference, PartialMessage]] = None,
        mention_author: Optional[bool] = None,
        view: Optional[View] = None,
        suppress_embeds: bool = False,
        ephemeral: bool = False,
        silent: bool = False,
        poll: Poll = MISSING,
    ) -> Message:
        """|coro|

        Sends a message to the destination with the content given.

        This works similarly to :meth:`~discord.abc.Messageable.send` for non-interaction contexts.

        For interaction based contexts this does one of the following:

        - :meth:`discord.InteractionResponse.send_message` if no response has been given.
        - A followup message if a response has been given.
        - Regular send if the interaction has expired

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` or
            :exc:`ValueError` instead of ``InvalidArgument``.

        Parameters
        ------------
        content: Optional[:class:`str`]
            The content of the message to send.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`~discord.Embed`
            The rich embed for the content.
        file: :class:`~discord.File`
            The file to upload.
        files: List[:class:`~discord.File`]
            A list of files to upload. Must be a maximum of 10.
        nonce: :class:`int`
            The nonce to use for sending this message. If the message was successfully sent,
            then the message will have a nonce with this value.
        delete_after: :class:`float`
            If provided, the number of seconds to wait in the background
            before deleting the message we just sent. If the deletion fails,
            then it is silently ignored.
        allowed_mentions: :class:`~discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`~discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`~discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`~discord.Client.allowed_mentions`
            are used instead.

            .. versionadded:: 1.4

        reference: Union[:class:`~discord.Message`, :class:`~discord.MessageReference`, :class:`~discord.PartialMessage`]
            A reference to the :class:`~discord.Message` to which you are replying, this can be created using
            :meth:`~discord.Message.to_reference` or passed directly as a :class:`~discord.Message`. You can control
            whether this mentions the author of the referenced message using the :attr:`~discord.AllowedMentions.replied_user`
            attribute of ``allowed_mentions`` or by setting ``mention_author``.

            This is ignored for interaction based contexts.

            .. versionadded:: 1.6

        mention_author: Optional[:class:`bool`]
            If set, overrides the :attr:`~discord.AllowedMentions.replied_user` attribute of ``allowed_mentions``.
            This is ignored for interaction based contexts.

            .. versionadded:: 1.6
        view: :class:`discord.ui.View`
            A Discord UI View to add to the message.

            .. versionadded:: 2.0
        embeds: List[:class:`~discord.Embed`]
            A list of embeds to upload. Must be a maximum of 10.

            .. versionadded:: 2.0
        stickers: Sequence[Union[:class:`~discord.GuildSticker`, :class:`~discord.StickerItem`]]
            A list of stickers to upload. Must be a maximum of 3. This is ignored for interaction based contexts.

            .. versionadded:: 2.0
        suppress_embeds: :class:`bool`
            Whether to suppress embeds for the message. This sends the message without any embeds if set to ``True``.

            .. versionadded:: 2.0
        ephemeral: :class:`bool`
            Indicates if the message should only be visible to the user who started the interaction.
            If a view is sent with an ephemeral message and it has no timeout set then the timeout
            is set to 15 minutes. **This is only applicable in contexts with an interaction**.

            .. versionadded:: 2.0
        silent: :class:`bool`
            Whether to suppress push and desktop notifications for the message. This will increment the mention counter
            in the UI, but will not actually send a notification.

            .. versionadded:: 2.2

        poll: :class:`~discord.Poll`
            The poll to send with this message.

            .. versionadded:: 2.4

        Raises
        --------
        ~discord.HTTPException
            Sending the message failed.
        ~discord.Forbidden
            You do not have the proper permissions to send the message.
        ValueError
            The ``files`` list is not of the appropriate size.
        TypeError
            You specified both ``file`` and ``files``,
            or you specified both ``embed`` and ``embeds``,
            or the ``reference`` object is not a :class:`~discord.Message`,
            :class:`~discord.MessageReference` or :class:`~discord.PartialMessage`.

        Returns
        ---------
        :class:`~discord.Message`
            The message that was sent.
        """
        return await self.ctx.send(
            content             = content,
            tts                 = tts,
            embed               = embed,
            embeds              = embeds,
            file                = file,
            files               = files,
            stickers            = stickers,
            delete_after        = delete_after,
            nonce               = nonce,
            allowed_mentions    = allowed_mentions,
            reference           = reference,
            mention_author      = mention_author,
            view                = view,
            suppress_embeds     = suppress_embeds,
            ephemeral           = ephemeral,
            silent              = silent,
            poll                = poll,
        )
# Version Globale: v00.00.00.pl
# Version du fichier: v00.00.00.1a
