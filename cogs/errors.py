from discord.ext import commands
from logpy import Logger
from logpy.ansi import BackgroundColor, Effect, ForegroundColor
from logpy.log import Format, Level

custom_format = Format("$date $time $level      $message", "%Y-%m-%d", "%H:%M:%S")
logger = Logger(custom_format)
err = Level("ERR", ForegroundColor.red, BackgroundColor.black, Effect.bold)

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("i searched the whole universe and still couldn't find that co")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("be more specific!! i need more info dummy")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("bad argument. get ratio'd mate")
        elif isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingRole):
            await ctx.send("u dont have the required perms or role")
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("this command is too LEWD for this channel (;𖦹ㅁ𖦹)")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"slowdown dude... retry in {error.retry_after:.2f} seconds")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("give me the power to do so")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"a dum error occured during invocation of command `{ctx.command.qualified_name}` inform the dev!!")
            logger.log(f"Error occurred in command {ctx.command.qualified_name}: {error}", err)
        elif isinstance(error, commands.NotOwner):
            await ctx.send("nah i aint listening to u")
        else:
            await ctx.send("An error occurred.")
            logger.log(f"An error occurred: {error}", err)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
