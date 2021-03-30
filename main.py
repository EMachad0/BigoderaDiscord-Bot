import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='?', description="BIGODERA", intents=intents)

startup_extensions = [
    "handles",
    "probleminha",
    "meme"
]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension("notebooks.extensions." + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    client.run(os.environ['DISCORD_TOKEN'])
