from typing         import Any, Union, Callable
from discord.ext    import commands
from asyncio        import iscoroutinefunction

kwargs_listeners: dict[str, Union[list[str], dict[str, Union[list[str], bool]]]] = {
    "on_discord_error": ["context"],
    "on_application_command": ["context"],
    "on_application_command_completion": ["context"],
    "on_application_command_error": ["context", "exception"],
    "on_unknown_application_command": ["interaction"],
    "on_audit_log_entry": ["entry"],
    "on_raw_audit_log_entry": ["payload"],
    "on_auto_moderation_rule_create": ["rule"],
    "on_auto_moderation_rule_update": ["rule"],
    "on_auto_moderation_rule_delete": ["rule"],
    "on_auto_moderation_action_execution": ["payload"],
    "on_member_ban": ["guild", "user"],
    "on_member_unban": ["guild", "user"],
    "on_private_channel_update": ["before", "after"],
    "on_private_channel_pins_update": ["channel", "last_pin"],
    "on_guild_channel_update": ["before", "after"],
    "on_guild_channel_pins_update": ["channel", "last_pin"],
    "on_guild_channel_delete": ["channel"],
    "on_guild_channel_create": ["channel"],
    "on_error":{
        "args": ["event"],
        "args&kwargs": True
    },
    "on_connect": [],
    "on_shard_connect": ["shard_id"],
    "on_disconnect": [],
    "on_shard_disconnect": ["shard_id"],
    "on_ready": [],
    "on_shard_ready": ["shard_id"],
    "on_resumed": [],
    "on_shard_resumed": ["shard_id"],
    "on_socket_event_type": ["event_type"],
    "on_socket_raw_receive": ["msg"],
    "on_socket_raw_send": ["payload"],
    "on_entitlement_create": ["entitlement"],
    "on_entitlement_update": ["entitlement"],
    "on_entitlement_delete": ["entitlement"],
    "on_guild_join": ["guild"],
    "on_guild_remove": ["guild"],
    "on_guild_update": ["before", "after"],
    "on_guild_role_create": ["role"],
    "on_guild_role_delete": ["role"],
    "on_guild_role_update": ["before", "after"],
    "on_guild_emojis_update": ["guild", "before", "after"],
    "on_guild_stickers_update": ["guild", "before", "after"],
    "on_guild_available": ["guild"],
    "on_guild_unavailable": ["guild"],
    "on_webhooks_update": ["channel"],
    "on_guild_integrations_update": ["guild"],
    "on_integration_create": ["integration"],
    "on_integration_update": ["integration"],
    "on_raw_integration_delete": ["payload"],
    "on_interaction": ["interaction"],
    "on_invite_create": ["invite"],
    "on_invite_delete": ["invite"],
    "on_member_join": ["member"],
    "on_member_remove": ["member"],
    "on_raw_member_remove": ["payload"],
    "on_member_update": ["before", "after"],
    "on_presence_update": ["before", "after"],
    "on_voice_state_update": ["member", "before", "after"],
    "on_user_update": ["before", "after"],
    "on_message": ["message"],
    "on_message_delete": ["message"],
    "on_bulk_message_delete": ["messages"],
    "on_raw_message_delete": ["payload"],
    "on_raw_bulk_message_delete": ["payload"],
    "on_message_edit": ["before", "after"],
    "on_raw_message_edit": ["payload"],
    "on_poll_vote_add": ["poll", "user", "answer"],
    "on_raw_poll_vote_add": ["payload"],
    "on_poll_vote_remove": ["poll", "user", "answer"],
    "on_raw_poll_vote_remove": ["payload"],
    "on_reaction_add": ["reaction", "user"],
    "on_raw_reaction_add": ["payload"],
    "on_reaction_remove": ["reaction", "user"],
    "on_raw_reaction_remove": ["payload"],
    "on_reaction_clear": ["message", "reactions"],
    "on_raw_reaction_clear": ["payload"],
    "on_reaction_clear_emoji": ["reaction"],
    "on_raw_reaction_clear_emoji": ["payload"],
    "on_scheduled_event_create": ["event"],
    "on_scheduled_event_update": ["before", "after"],
    "on_scheduled_event_delete": ["event"],
    "on_scheduled_event_user_add": ["event", "member"],
    "on_raw_scheduled_event_user_add": ["payload"],
    "on_scheduled_event_user_remove": ["event", "member"],
    "on_raw_scheduled_event_user_remove": ["payload"],
    "on_stage_instance_create": ["stage_instance"],
    "on_stage_instance_delete": ["stage_instance"],
    "on_stage_instance_update": ["before", "after"],
    "on_thread_join": ["thread"],
    "on_thread_create": ["thread"],
    "on_thread_remove": ["thread"],
    "on_thread_delete": ["thread"],
    "on_raw_thread_delete": ["payload"],
    "on_thread_member_join": ["member"],
    "on_thread_member_remove": ["member"],
    "on_raw_thread_member_remove": ["payload"],
    "on_thread_update": ["before", "after"],
    "on_raw_thread_update": ["payload"],
    "on_typing": ["channel", "user", "when"],
    "on_raw_typing": ["payload"],
    "on_voice_channel_status_update": ["channel", "before", "after"],
    "on_raw_voice_channel_status_update": ["payload"]
}

class AllListeners(commands.Cog):
    def __init__(self, callback: Callable[[str, list[Any], dict[str, Any]], Any]) -> None:
        self.__callback: Callable = callback

    @commands.Cog.listener("on_discord_error")
    async def _on_discord_error(self, *args):
        await self._on_event("on_discord_error", list(args))

    @commands.Cog.listener("on_application_command")
    async def _on_application_command(self, *args):
        """Called when an application command is received."""
        await self._on_event("on_application_command", list(args))

    @commands.Cog.listener("on_application_command_completion")
    async def _on_application_command_completion(self, *args):
        """Called when an application command is completed, after any checks have finished."""
        await self._on_event("on_application_command_completion", list(args))

    @commands.Cog.listener("on_application_command_error")
    async def _on_application_command_error(self, *args):
        """Called when an application command has an error."""
        await self._on_event("on_application_command_error", list(args))

    @commands.Cog.listener("on_unknown_application_command")
    async def _on_unknown_application_command(self, *args):
        """Called when an application command was not found in the bot’s internal cache."""
        await self._on_event("on_unknown_application_command", list(args))

    @commands.Cog.listener("on_audit_log_entry")
    async def _on_audit_log_entry(self, *args):
        """Called when an audit log entry is created."""
        await self._on_event("on_audit_log_entry", list(args))

    @commands.Cog.listener("on_raw_audit_log_entry")
    async def _on_raw_audit_log_entry(self, *args):
        """Called when an audit log entry is created, regardless of the state of the internal user cache."""
        await self._on_event("on_raw_audit_log_entry", list(args))

    @commands.Cog.listener("on_auto_moderation_rule_create")
    async def _on_auto_moderation_rule_create(self, *args):
        """Called when an auto moderation rule is created."""
        await self._on_event("on_auto_moderation_rule_create", list(args))

    @commands.Cog.listener("on_auto_moderation_rule_update")
    async def _on_auto_moderation_rule_update(self, *args):
        """Called when an auto moderation rule is updated."""
        await self._on_event("on_auto_moderation_rule_update", list(args))

    @commands.Cog.listener("on_auto_moderation_rule_delete")
    async def _on_auto_moderation_rule_delete(self, *args):
        """Called when an auto moderation rule is deleted."""
        await self._on_event("on_auto_moderation_rule_delete", list(args))

    @commands.Cog.listener("on_auto_moderation_action_execution")
    async def _on_auto_moderation_action_execution(self, *args):
        """Called when an auto moderation action is executed."""
        await self._on_event("on_auto_moderation_action_execution", list(args))

    @commands.Cog.listener("on_member_ban")
    async def _on_member_ban(self, *args):
        """Called when a user gets banned from a Guild."""
        await self._on_event("on_member_ban", list(args))

    @commands.Cog.listener("on_member_unban")
    async def _on_member_unban(self, *args):
        """Called when a user gets unbanned from a Guild."""
        await self._on_event("on_member_unban", list(args))

    @commands.Cog.listener("on_private_channel_update")
    async def _on_private_channel_update(self, *args):
        """Called whenever a private group DM is updated."""
        await self._on_event("on_private_channel_update", list(args))

    @commands.Cog.listener("on_private_channel_pins_update")
    async def _on_private_channel_pins_update(self, *args):
        """Called whenever a message is pinned or unpinned from a private channel."""
        await self._on_event("on_private_channel_pins_update", list(args))

    @commands.Cog.listener("on_guild_channel_update")
    async def _on_guild_channel_update(self, *args):
        """Called whenever a guild channel is updated."""
        await self._on_event("on_guild_channel_update", list(args))

    @commands.Cog.listener("on_guild_channel_pins_update")
    async def _on_guild_channel_pins_update(self, *args):
        """Called whenever a message is pinned or unpinned from a guild channel."""
        await self._on_event("on_guild_channel_pins_update", list(args))

    @commands.Cog.listener("on_guild_channel_delete")
    async def _on_guild_channel_delete(self, *args):
        """Called whenever a guild channel is deleted."""
        await self._on_event("on_guild_channel_delete", list(args))

    @commands.Cog.listener("on_guild_channel_create")
    async def _on_guild_channel_create(self, *args):
        """Called whenever a guild channel is created."""
        await self._on_event("on_guild_channel_create", list(args))

    @commands.Cog.listener("on_error")
    async def _on_error(self, *args, **kwargs):
        """Called when an uncaught exception occurs."""
        await self._on_event("on_error", list(args), kwargs)

    @commands.Cog.listener("on_connect")
    async def _on_connect(self, *args):
        """Called when the client has successfully connected to Discord."""
        await self._on_event("on_connect", list(args))

    @commands.Cog.listener("on_shard_connect")
    async def _on_shard_connect(self, *args):
        """Similar to on_connect() but used by AutoShardedClient when a particular shard ID connects."""
        await self._on_event("on_shard_connect", list(args))

    @commands.Cog.listener("on_disconnect")
    async def _on_disconnect(self, *args):
        """Called when the client disconnects from Discord."""
        await self._on_event("on_disconnect", list(args))

    @commands.Cog.listener("on_shard_disconnect")
    async def _on_shard_disconnect(self, *args):
        """Similar to on_disconnect() but used by AutoShardedClient when a particular shard ID disconnects."""
        await self._on_event("on_shard_disconnect", list(args))

    @commands.Cog.listener("on_ready")
    async def _on_ready(self, *args):
        """Called when the client is done preparing the data received from Discord."""
        await self._on_event("on_ready", list(args))

    @commands.Cog.listener("on_shard_ready")
    async def _on_shard_ready(self, *args):
        """Similar to on_ready() but used by AutoShardedClient when a particular shard ID is ready."""
        await self._on_event("on_shard_ready", list(args))

    @commands.Cog.listener("on_resumed")
    async def _on_resumed(self, *args):
        """Called when the client resumes a session."""
        await self._on_event("on_resumed", list(args))

    @commands.Cog.listener("on_shard_resumed")
    async def _on_shard_resumed(self, *args):
        """Similar to on_resumed() but used by AutoShardedClient when a particular shard ID resumes a session."""
        await self._on_event("on_shard_resumed", list(args))

    @commands.Cog.listener("on_socket_event_type")
    async def _on_socket_event_type(self, *args):
        """Called whenever a WebSocket event is received from the WebSocket."""
        await self._on_event("on_socket_event_type", list(args))

    @commands.Cog.listener("on_socket_raw_receive")
    async def _on_socket_raw_receive(self, *args):
        """Called whenever a message is completely received from the WebSocket."""
        await self._on_event("on_socket_raw_receive", list(args))

    @commands.Cog.listener("on_socket_raw_send")
    async def _on_socket_raw_send(self, *args):
        """Called whenever a send operation is done on the WebSocket before the message is sent."""
        await self._on_event("on_socket_raw_send", list(args))

    @commands.Cog.listener("on_entitlement_create")
    async def _on_entitlement_create(self, *args):
        """Called when a user subscribes to an SKU."""
        await self._on_event("on_entitlement_create", list(args))

    @commands.Cog.listener("on_entitlement_update")
    async def _on_entitlement_update(self, *args):
        """Called when a user’s subscription to an Entitlement is renewed for the next billing period."""
        await self._on_event("on_entitlement_update", list(args))

    @commands.Cog.listener("on_entitlement_delete")
    async def _on_entitlement_delete(self, *args):
        """Called when a user’s entitlement is deleted."""
        await self._on_event("on_entitlement_delete", list(args))

    @commands.Cog.listener("on_guild_join")
    async def _on_guild_join(self, *args):
        """Called when a Guild is either created by the Client or when the Client joins a guild."""
        await self._on_event("on_guild_join", list(args))

    @commands.Cog.listener("on_guild_remove")
    async def _on_guild_remove(self, *args):
        """Called when a Guild is removed from the Client."""
        await self._on_event("on_guild_remove", list(args))

    @commands.Cog.listener("on_guild_update")
    async def _on_guild_update(self, *args):
        """Called when a Guild is updated."""
        await self._on_event("on_guild_update", list(args))

    @commands.Cog.listener("on_guild_role_create")
    async def _on_guild_role_create(self, *args):
        """Called when a Guild creates a Role."""
        await self._on_event("on_guild_role_create", list(args))

    @commands.Cog.listener("on_guild_role_delete")
    async def _on_guild_role_delete(self, *args):
        """Called when a Guild deletes a Role."""
        await self._on_event("on_guild_role_delete", list(args))

    @commands.Cog.listener("on_guild_role_update")
    async def _on_guild_role_update(self, *args):
        """Called when a Role is changed guild-wide."""
        await self._on_event("on_guild_role_update", list(args))

    @commands.Cog.listener("on_guild_emojis_update")
    async def _on_guild_emojis_update(self, *args):
        """Called when a Guild adds or removes an Emoji."""
        await self._on_event("on_guild_emojis_update", list(args))

    @commands.Cog.listener("on_guild_stickers_update")
    async def _on_guild_stickers_update(self, *args):
        """Called when a Guild adds or removes a sticker."""
        await self._on_event("on_guild_stickers_update", list(args))

    @commands.Cog.listener("on_guild_available")
    async def _on_guild_available(self, *args):
        """Called when a guild becomes available."""
        await self._on_event("on_guild_available", list(args))

    @commands.Cog.listener("on_guild_unavailable")
    async def _on_guild_unavailable(self, *args):
        """Called when a guild becomes unavailable."""
        await self._on_event("on_guild_unavailable", list(args))

    @commands.Cog.listener("on_webhooks_update")
    async def _on_webhooks_update(self, *args):
        """Called whenever a webhook is created, modified, or removed from a guild channel."""
        await self._on_event("on_webhooks_update", list(args))

    @commands.Cog.listener("on_guild_integrations_update")
    async def _on_guild_integrations_update(self, *args):
        """Called whenever an integration is created, modified, or removed from a guild."""
        await self._on_event("on_guild_integrations_update", list(args))

    @commands.Cog.listener("on_integration_create")
    async def _on_integration_create(self, *args):
        """Called when an integration is created."""
        await self._on_event("on_integration_create", list(args))

    @commands.Cog.listener("on_integration_update")
    async def _on_integration_update(self, *args):
        """Called when an integration is updated."""
        await self._on_event("on_integration_update", list(args))

    @commands.Cog.listener("on_raw_integration_delete")
    async def _on_raw_integration_delete(self, *args):
        """Called when an integration is deleted."""
        await self._on_event("on_raw_integration_delete", list(args))

    @commands.Cog.listener("on_interaction")
    async def _on_interaction(self, *args):
        """Called when an interaction happens."""
        await self._on_event("on_interaction", list(args))

    @commands.Cog.listener("on_invite_create")
    async def _on_invite_create(self, *args):
        """Called when an Invite is created."""
        await self._on_event("on_invite_create", list(args))

    @commands.Cog.listener("on_invite_delete")
    async def _on_invite_delete(self, *args):
        """Called when an Invite is deleted."""
        await self._on_event("on_invite_delete", list(args))

    @commands.Cog.listener("on_member_join")
    async def _on_member_join(self, *args):
        """Called when a Member joins a Guild."""
        await self._on_event("on_member_join", list(args))

    @commands.Cog.listener("on_member_remove")
    async def _on_member_remove(self, *args):
        """Called when a Member leaves a Guild."""
        await self._on_event("on_member_remove", list(args))

    @commands.Cog.listener("on_raw_member_remove")
    async def _on_raw_member_remove(self, *args):
        """Called when a Member leaves a Guild, regardless of the internal member cache."""
        await self._on_event("on_raw_member_remove", list(args))

    @commands.Cog.listener("on_member_update")
    async def _on_member_update(self, *args):
        """Called when a Member updates their profile."""
        await self._on_event("on_member_update", list(args))

    @commands.Cog.listener("on_presence_update")
    async def _on_presence_update(self, *args):
        """Called when a Member updates their presence."""
        await self._on_event("on_presence_update", list(args))

    @commands.Cog.listener("on_voice_state_update")
    async def _on_voice_state_update(self, *args):
        """Called when a Member changes their VoiceState."""
        await self._on_event("on_voice_state_update", list(args))

    @commands.Cog.listener("on_user_update")
    async def _on_user_update(self, *args):
        """Called when a User updates their profile."""
        await self._on_event("on_user_update", list(args))

    @commands.Cog.listener("on_message")
    async def _on_message(self, *args):
        """Called when a Message is created and sent."""
        await self._on_event("on_message", list(args))

    @commands.Cog.listener("on_message_delete")
    async def _on_message_delete(self, *args):
        """Called when a message is deleted."""
        await self._on_event("on_message_delete", list(args))

    @commands.Cog.listener("on_bulk_message_delete")
    async def _on_bulk_message_delete(self, *args):
        """Called when messages are bulk deleted."""
        await self._on_event("on_bulk_message_delete", list(args))

    @commands.Cog.listener("on_raw_message_delete")
    async def _on_raw_message_delete(self, *args):
        """Called when a message is deleted, regardless of cache state."""
        await self._on_event("on_raw_message_delete", list(args))

    @commands.Cog.listener("on_raw_bulk_message_delete")
    async def _on_raw_bulk_message_delete(self, *args):
        """Called when messages are bulk deleted, regardless of cache state."""
        await self._on_event("on_raw_bulk_message_delete", list(args))

    @commands.Cog.listener("on_message_edit")
    async def _on_message_edit(self, *args):
        """Called when a Message receives an update event."""
        await self._on_event("on_message_edit", list(args))

    @commands.Cog.listener("on_raw_message_edit")
    async def _on_raw_message_edit(self, *args):
        """Called when a message is edited, regardless of cache state."""
        await self._on_event("on_raw_message_edit", list(args))

    @commands.Cog.listener("on_poll_vote_add")
    async def _on_poll_vote_add(self, *args):
        """Called when a vote is cast on a poll."""
        await self._on_event("on_poll_vote_add", list(args))

    @commands.Cog.listener("on_raw_poll_vote_add")
    async def _on_raw_poll_vote_add(self, *args):
        """Called when a vote is cast on a poll, regardless of cache state."""
        await self._on_event("on_raw_poll_vote_add", list(args))

    @commands.Cog.listener("on_poll_vote_remove")
    async def _on_poll_vote_remove(self, *args):
        """Called when a vote is removed from a poll."""
        await self._on_event("on_poll_vote_remove", list(args))

    @commands.Cog.listener("on_raw_poll_vote_remove")
    async def _on_raw_poll_vote_remove(self, *args):
        """Called when a vote is removed from a poll, regardless of cache state."""
        await self._on_event("on_raw_poll_vote_remove", list(args))

    @commands.Cog.listener("on_reaction_add")
    async def _on_reaction_add(self, *args):
        """Called when a message has a reaction added to it."""
        await self._on_event("on_reaction_add", list(args))

    @commands.Cog.listener("on_raw_reaction_add")
    async def _on_raw_reaction_add(self, *args):
        """Called when a message has a reaction added, regardless of cache state."""
        await self._on_event("on_raw_reaction_add", list(args))

    @commands.Cog.listener("on_reaction_remove")
    async def _on_reaction_remove(self, *args):
        """Called when a message has a reaction removed from it."""
        await self._on_event("on_reaction_remove", list(args))

    @commands.Cog.listener("on_raw_reaction_remove")
    async def _on_raw_reaction_remove(self, *args):
        """Called when a message has a reaction removed, regardless of cache state."""
        await self._on_event("on_raw_reaction_remove", list(args))

    @commands.Cog.listener("on_reaction_clear")
    async def _on_reaction_clear(self, *args):
        """Called when a message has all its reactions removed."""
        await self._on_event("on_reaction_clear", list(args))

    @commands.Cog.listener("on_raw_reaction_clear")
    async def _on_raw_reaction_clear(self, *args):
        """Called when a message has all its reactions removed, regardless of cache state."""
        await self._on_event("on_raw_reaction_clear", list(args))

    @commands.Cog.listener("on_reaction_clear_emoji")
    async def _on_reaction_clear_emoji(self, *args):
        """Called when a message has a specific reaction removed."""
        await self._on_event("on_reaction_clear_emoji", list(args))

    @commands.Cog.listener("on_raw_reaction_clear_emoji")
    async def _on_raw_reaction_clear_emoji(self, *args):
        """Called when a message has a specific reaction removed, regardless of cache state."""
        await self._on_event("on_raw_reaction_clear_emoji", list(args))

    @commands.Cog.listener("on_scheduled_event_create")
    async def _on_scheduled_event_create(self, *args):
        """Called when a ScheduledEvent is created."""
        await self._on_event("on_scheduled_event_create", list(args))

    @commands.Cog.listener("on_scheduled_event_update")
    async def _on_scheduled_event_update(self, *args):
        """Called when a ScheduledEvent is updated."""
        await self._on_event("on_scheduled_event_update", list(args))

    @commands.Cog.listener("on_scheduled_event_delete")
    async def _on_scheduled_event_delete(self, *args):
        """Called when a ScheduledEvent is deleted."""
        await self._on_event("on_scheduled_event_delete", list(args))

    @commands.Cog.listener("on_scheduled_event_user_add")
    async def _on_scheduled_event_user_add(self, *args):
        """Called when a user subscribes to an event."""
        await self._on_event("on_scheduled_event_user_add", list(args))

    @commands.Cog.listener("on_raw_scheduled_event_user_add")
    async def _on_raw_scheduled_event_user_add(self, *args):
        """Called when a user subscribes to an event, regardless of cache state."""
        await self._on_event("on_raw_scheduled_event_user_add", list(args))

    @commands.Cog.listener("on_scheduled_event_user_remove")
    async def _on_scheduled_event_user_remove(self, *args):
        """Called when a user unsubscribes from an event."""
        await self._on_event("on_scheduled_event_user_remove", list(args))

    @commands.Cog.listener("on_raw_scheduled_event_user_remove")
    async def _on_raw_scheduled_event_user_remove(self, *args):
        """Called when a user unsubscribes from an event, regardless of cache state."""
        await self._on_event("on_raw_scheduled_event_user_remove", list(args))

    @commands.Cog.listener("on_stage_instance_create")
    async def _on_stage_instance_create(self, *args):
        """Called when a StageInstance is created."""
        await self._on_event("on_stage_instance_create", list(args))

    @commands.Cog.listener("on_stage_instance_delete")
    async def _on_stage_instance_delete(self, *args):
        """Called when a StageInstance is deleted."""
        await self._on_event("on_stage_instance_delete", list(args))

    @commands.Cog.listener("on_stage_instance_update")
    async def _on_stage_instance_update(self, *args):
        """Called when a StageInstance is updated."""
        await self._on_event("on_stage_instance_update", list(args))

    @commands.Cog.listener("on_thread_join")
    async def _on_thread_join(self, *args):
        """Called whenever a thread is joined."""
        await self._on_event("on_thread_join", list(args))

    @commands.Cog.listener("on_thread_create")
    async def _on_thread_create(self, *args):
        """Called whenever a thread is created."""
        await self._on_event("on_thread_create", list(args))

    @commands.Cog.listener("on_thread_remove")
    async def _on_thread_remove(self, *args):
        """Called whenever a thread is removed."""
        await self._on_event("on_thread_remove", list(args))

    @commands.Cog.listener("on_thread_delete")
    async def _on_thread_delete(self, *args):
        """Called whenever a thread is deleted."""
        await self._on_event("on_thread_delete", list(args))

    @commands.Cog.listener("on_raw_thread_delete")
    async def _on_raw_thread_delete(self, *args):
        """Called whenever a thread is deleted, regardless of cache state."""
        await self._on_event("on_raw_thread_delete", list(args))

    @commands.Cog.listener("on_thread_member_join")
    async def _on_thread_member_join(self, *args):
        """Called when a ThreadMember joins a Thread."""
        await self._on_event("on_thread_member_join", list(args))

    @commands.Cog.listener("on_thread_member_remove")
    async def _on_thread_member_remove(self, *args):
        """Called when a ThreadMember leaves a Thread."""
        await self._on_event("on_thread_member_remove", list(args))

    @commands.Cog.listener("on_raw_thread_member_remove")
    async def _on_raw_thread_member_remove(self, *args):
        """Called when a ThreadMember leaves a Thread, regardless of cache state."""
        await self._on_event("on_raw_thread_member_remove", list(args))

    @commands.Cog.listener("on_thread_update")
    async def _on_thread_update(self, *args):
        """Called whenever a thread is updated."""
        await self._on_event("on_thread_update", list(args))

    @commands.Cog.listener("on_raw_thread_update")
    async def _on_raw_thread_update(self, *args):
        """Called whenever a thread is updated, regardless of cache state."""
        await self._on_event("on_raw_thread_update", list(args))

    @commands.Cog.listener("on_typing")
    async def _on_typing(self, *args):
        """Called when someone begins typing a message."""
        await self._on_event("on_typing", list(args))

    @commands.Cog.listener("on_raw_typing")
    async def _on_raw_typing(self, *args):
        """Called when someone begins typing a message, regardless of cache state."""
        await self._on_event("on_raw_typing", list(args))

    @commands.Cog.listener("on_voice_channel_status_update")
    async def _on_voice_channel_status_update(self, *args):
        """Called when someone updates a voice channel status."""
        await self._on_event("on_voice_channel_status_update", list(args))

    @commands.Cog.listener("on_raw_voice_channel_status_update")
    async def _on_raw_voice_channel_status_update(self, *args):
        """Called when someone updates a voice channels status."""
        await self._on_event("on_raw_voice_channel_status_update", list(args))

    async def _on_event(self, event: str, args: list[Any], kwargs: dict[str, Any] = {}) -> None:
        """Dispatch the event to all regist ered listeners."""
        try:
            await self.__callback(event, *args, **kwargs)
        except Exception as e:
            print(f"Exection in listeners.py: {e}")
# Version Globale: v00.00.00.pl
# Version du fichier: v00.00.00.03
