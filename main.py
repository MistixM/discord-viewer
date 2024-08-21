import discord
import configparser
import random
import aiohttp

from discord.ext import commands

def main():
    # Initialize and read configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Set up Discord bot and intents
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    # Set up bot prefix and intents
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Commands
    @bot.command(name="hello", help="bot will say hi to you! Cute, isn't it..?")
    async def hey(ctx):
        await ctx.reply(f"Hey there, {ctx.author.global_name} 👋", mention_author=True)

    @bot.command(name="roll", help="bot will give you random number (from 0 to 100). Owner got 0!")
    async def roll(ctx):
        await ctx.reply(f"{generate_random_number()} {random.choice(['🚀', '🍀', '⚠️', '🔥', '🤩'])}")
    
    @bot.command(name="info", help='Are you FBI agent? Anyway, bot will give you all server details.')
    async def get_info(ctx):
        guild = bot.guilds[0]

        await ctx.send(f"📝 Alright, here's server information:\n\n- Server owner: **{guild.owner}**\n\n- Server name: **{guild.name}**\n\n- Members: **{guild.member_count}**\n\n- Server description: **{guild.description}**")

    @bot.command(name="joke", help="Never gonna give u up.. The bot will joke for you.")
    async def tell_a_joke(ctx):
        joke_api = config['Discord']['JOKE_API']
        
        joke_url = f"https://api.humorapi.com/jokes/random?api-key={joke_api}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(joke_url) as response:

                data = await response.json()
                joke = data.get('joke', 'No joke found')

                await ctx.reply(f"😄 {joke}")

    # Handle errors here
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("🫤 Oh, swap! Sorry, I don't recognize that command. Type `!help` to see a list of available commands.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("⚠️ You don't have the required permissions to use this command.")
        else:
            print(f"An unexpected error occurred: {error}. Please try again.")

    # Initialize bot with TOKEN in .ini file and run it
    bot.run(str(config['Discord']['TOKEN']))

# Well, it's generate random number using random library =)
def generate_random_number():
    return random.randint(0, 100)


if __name__ == "__main__":
    main()
