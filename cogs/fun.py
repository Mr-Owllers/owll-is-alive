import json
import random
import discord
from discord.ext import commands

class Fun(commands.Cog, description="Fun commands"):
    """ Fun commands """
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help="YEET!")
    async def yeet(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻ YEEEEEEEET!!!!")

    @commands.hybrid_command(help="hmmm...")
    async def unyeet(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @commands.hybrid_command(help="Roll a dice")
    async def roll(self, ctx):
        await ctx.send(f":game_die: You rolled a {random.randint(1, 6)}")

    @commands.hybrid_command(help="Flip a coin")
    async def flip(self, ctx):
        await ctx.send(f":coin: You flipped a {random.choice(['Heads', 'Tails'])}")

    @commands.hybrid_command(help="Say something")
    async def say(self, ctx, *, message):
        await ctx.send(message)

    @commands.hybrid_command(help="Say something in an embed")
    async def embed(self, ctx, title: str=None, *, message):
        embed = discord.Embed(
            title=title,
            description=message,
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(help="Ask the ball", name="11ball")
    async def ball(self, ctx, *, question):
        responses = json.loads(open("../responses.json", "r").read())
        await ctx.send(
            f"Question: {ctx.options.question}\nAnswer: {random.choice(responses)}"
        )
        
    # rock paper scissors
    @commands.hybrid_command(help="Rock, Paper, Scissors")
    async def rps(self, ctx, choice):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        if choice.lower() in choices:
            if choice.lower() == bot_choice:
                await ctx.send(f"Bot chose {bot_choice}, it's a tie!")
            elif choice.lower() == "rock" and bot_choice == "scissors":
                await ctx.send(f"Bot chose {bot_choice}, you win!")
            elif choice.lower() == "paper" and bot_choice == "rock":
                await ctx.send(f"Bot chose {bot_choice}, you win!")
            elif choice.lower() == "scissors" and bot_choice == "paper":
                await ctx.send(f"Bot chose {bot_choice}, you win!")
            else:
                await ctx.send(f"Bot chose {bot_choice}, you lose!")
        else:
            await ctx.send("Invalid choice, please choose rock, paper, or scissors")
            
    @commands.hybrid_command(help="Guess a random number")
    async def guess(self, ctx):
        number = random.randint(1, 100)
        await ctx.send("I'm thinking of a number between 1 and 100, what is it? type 'im_a_loser' to be a loser")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while True:
                guess = await self.bot.wait_for("message", check=check)
                if guess.content.isdigit():
                    if int(guess.content) == number:
                        await ctx.send(f"Congratulations! The number was {number}")
                        break
                    elif int(guess.content) > number:
                        await ctx.send("Too high!")
                    elif int(guess.content) < number:
                        await ctx.send("Too low!")
                elif guess.content.lower() == "im_a_loser":
                    await ctx.send(f"The number was {number}, loser!")
                    break
                else:
                    await ctx.send("Invalid input, please enter a number")
            
    @commands.hybrid_command(help="Fight the bot")
    async def fight(self, ctx):
        await ctx.send("1v1 les go! type 'im_a_loser' to be a loser")
        bot_health = 10
        player_health = 10
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while bot_health > 0 and player_health > 0:
            player_attack = random.randint(-10, 10)
            bot_attack = random.randint(-10, 10)
            await ctx.send(f"your health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}\nChoose your attack: punch, kick, bite, spell, or heal")
            choices = ["punch", "kick", "bite", "spell", "heal"]
            player_choice = await self.bot.wait_for("message", check=check)
            
            player_health = min(player_health, 20)
            bot_health = min(bot_health, 20)
            
            if player_choice.content.lower() in choices:
                if player_choice.content.lower() == "punch":
                    weak = ["your punch was so weak, it healed the bot", "you missed", "was that a punch or a tickle?", "you failed to even make a fist", "HAHAHA WHAT WAS THAT??!"]
                    strong = ["you landed a solid punch", "you hit the bot", "you punched the bot", "you landed a punch", "you punched the bot in the face"]
                    if player_attack <= 0:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(weak)}\nbot gained {-player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                    else:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(strong)}\nbot lost {player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                elif player_choice.content.lower() == "kick":
                    weak = ["your kick was so weak, it healed the bot", "you missed", "was that a kick or a tap?", "you failed to even lift your leg", "HAHAHA WHAT WAS THAT??!"]
                    strong = ["you landed a solid kick", "you hit the bot", "you kicked the bot", "you landed a kick", "you kicked the bot in the face"]
                    if player_attack <= 0:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(weak)}\nbot gained {-player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                    else:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(strong)}\nbot lost {player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                elif player_choice.content.lower() == "bite":   
                    weak = ["your bite was so weak, it healed the bot", "you missed", "was that a bite or a lick?", "you failed to even open your mouth", "HAHAHA WHAT WAS THAT??!"]
                    strong = ["you landed a solid bite", "you hit the bot", "you bit the bot", "you landed a bite", "you bit the bot in the face"]
                    if player_attack <= 0:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(weak)}\nbot gained {-player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                    else:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(strong)}\nbot lost {player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                elif player_choice.content.lower() == "spell":
                    weak = ["your spell was so weak, it healed the bot", "you missed", "was that a spell or a yawn?", "you failed to even cast a spell", "HAHAHA WHAT WAS THAT??!"]
                    strong = ["you landed a solid spell", "you hit the bot", "you cast a spell on the bot", "you landed a spell", "you cast a spell on the bot"]
                    if player_attack <= 0:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(weak)}\nbot gained {-player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                    else:
                        bot_health -= player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(strong)}\nbot lost {player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                elif player_choice.content.lower() == "heal":
                    weak = ["your heal was so weak, it made you lose health instead", "you missed, somehow", "are you healing yourself or the rock?", "you failed to even start the healing process", "HOW DO YOU EVEN FAIL AT THAT??!"]
                    strong = ["you landed a solid heal", "you healed yourself", "you healed", "you healed yourself", "you healed yourself"]
                    if player_attack <= 0:
                        player_health += player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(weak)}\nyou lost {-player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                    else:
                        player_health += player_attack
                        await ctx.send(f"you chose: {player_choice.content}\n{random.choice(strong)}\nyou gained {player_attack} health\nyour health: {min(player_health, 20)}\nbot health: {min(bot_health, 20)}")
                
                bot_choice = random.choice(choices)
                if bot_choice == "punch":
                    weak = ["the bot's punch was so weak, it healed you", "the bot missed", "was that a punch or a tickle?", "the bot failed to even make a fist", "LOL THE BOT CAN'T EVEN PUNCH"]
                    strong = ["the bot landed a solid punch", "the bot hit you", "the bot punched you", "the bot landed a punch", "the bot punched you in the face"]
                    if bot_attack <= 0:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(weak)}\nyou gained {-bot_attack} health\n")
                    else:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(strong)}\nyou lost {bot_attack} health\n")
                elif bot_choice == "kick":
                    weak = ["the bot's kick was so weak, it healed you", "the bot missed", "was that a kick or a tap?", "the bot failed to even lift its leg", "LOL THE BOT CAN'T EVEN KICK"]
                    strong = ["the bot landed a solid kick", "the bot hit you", "the bot kicked you", "the bot landed a kick", "the bot kicked you in the face"]
                    if bot_attack <= 0:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(weak)}\nyou gained {-bot_attack} health\n")
                    else:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(strong)}\nyou lost {bot_attack} health\n")
                elif bot_choice == "bite":   
                    weak = ["the bot's bite was so weak, it healed you", "the bot missed", "was that a bite or a lick?", "the bot failed to even open its mouth", "LOL THE BOT CAN'T EVEN BITE"]
                    strong = ["the bot landed a solid bite", "the bot hit you", "the bot bit you", "the bot landed a bite", "the bot bit you in the face"]
                    if bot_attack <= 0:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(weak)}\nyou gained {-bot_attack} health\n")
                    else:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(strong)}\nyou lost {bot_attack} health\n")
                elif bot_choice == "spell":
                    weak = ["the bot's spell was so weak, it healed you", "the bot missed", "was that a spell or a yawn?", "the bot failed to even cast a spell", "LOL THE BOT CAN'T EVEN SPELL"]
                    strong = ["the bot landed a solid spell", "the bot hit you", "the bot cast a spell on you", "the bot landed a spell", "the bot cast a spell on you"]
                    if bot_attack <= 0:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(weak)}\nyou gained {-bot_attack} health\n")
                    else:
                        player_health -= bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(strong)}\nyou lost {bot_attack} health\n")
                elif bot_choice == "heal":
                    weak = ["the bot's heal was so weak, it made you lose health instead", "the bot missed, somehow", "is the bot healing itself or the rock?", "the bot failed to even start the healing process", "HOW DOES THE BOT EVEN FAIL AT THAT??!"]
                    strong = ["the bot landed a solid heal", "the bot healed itself", "the bot healed", "the bot healed itself", "the bot healed itself"]
                    if bot_attack <= 0:
                        bot_health += bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(weak)}\nbot lost {-bot_attack} health\n")
                    else:
                        bot_health += bot_attack
                        await ctx.send(f"the bot chose: {bot_choice}\n{random.choice(strong)}\nbot gained {bot_attack} health\n")
            elif player_choice.content.lower() == "im_a_loser":
                await ctx.send("hahaha loser!")
                break
            else:
                player_health -= 1
                await ctx.send("Invalid choice, please choose punch, kick, bite, spell, or heal. You lost 1 health as a penalty")
                
            if bot_health <= 0: 
                await ctx.send("You win! bot's health reached 0")
                break
            elif player_health <= 0:
                await ctx.send("You lose! your health reached 0")
                break
                
        
async def setup(bot):
    await bot.add_cog(Fun(bot))