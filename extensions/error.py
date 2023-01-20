import hikari
import lightbulb

plugin = lightbulb.Plugin('error', 'error handlers for the commands.')

# Error Handler for bot commands
@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("Not enough arguments in user's input.")
    elif isinstance(exception, lightbulb.NSFWChannelOnly):
        await event.context.respond("This command is restricted to only being used in NSFW channels.")
    elif isinstance(exception, lightbulb.BotOnly):
        await event.context.respond("This command is restricted to only being used by Bots.")
    elif isinstance(exception, lightbulb.BotMissingRequiredPermission):
        await event.context.respond("Bot missing one or more permissions required to run this command.")
    elif isinstance(exception, lightbulb.MissingRequiredRole) or isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond("User missing role or permission required to run this command.")
    else:
        raise exception

def load(client):
    client.add_plugin(plugin)
