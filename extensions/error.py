import hikari
import lightbulb

plugin = lightbulb.Plugin('error', 'error handlers for the commands.')

# Error Handler for bot commands
@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"bruh a dum error occured during invocation of command `{event.context.command.name}`... check terminal!")
        raise event.exception
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("you aint my owner")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"slowdown... retry in `{exception.retry_after:.2f}` seconds!")
    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("be more specific")
    elif isinstance(exception, lightbulb.NSFWChannelOnly):
        await event.context.respond("this command is too LEWD for this channel (;𖦹ㅁ𖦹)")
    elif isinstance(exception, lightbulb.CommandNotFound):
        await event.context.respond("i searched the whole universe and still couldn't find that command")
    elif isinstance(exception, lightbulb.BotMissingRequiredPermission):
        await event.context.respond("gimme perms first")
    elif isinstance(exception, lightbulb.MissingRequiredRole) or isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond("u dont have the required perms or role")
    else:
        raise exception

def load(client):
    client.add_plugin(plugin)
