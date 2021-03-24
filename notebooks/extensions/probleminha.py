from discord.ext import commands

from notebooks import cf_api
from notebooks.DAO import HandleDB


class Probleminha(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('$probleminha'):
            content = message.content.split()
            if len(content) == 1:
                await message.channel.send("rating?")
                return
            rating = content[1]
            tags = {t.replace('_', ' ') for t in content[2:]}
            handle = HandleDB.select(message.author.name + '#' + message.author.discriminator)
            try:
                problem = cf_api.get_codeforces_problem(handle, rating, tags)
                await message.channel.send(problem)
            except Exception as e:
                print(f'Exception {e}: {e.args}')
                await message.channel.send(e.args[0])


def setup(bot):
    bot.add_cog(Probleminha(bot))

