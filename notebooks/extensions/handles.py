import discord
from notebooks import cf_api
from notebooks.DAO import HandleDB
from discord.ext import commands, tasks


class Handles(commands.Cog):
    roles = ["Unrated", "Newbie", "Pupil", "Specialist", "Expert", "Candidate Master", "Grandmaster"]
    brute_guild_id = 599810003347701792

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.update_roles_daily.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('$register'):
            handle = message.content.split()[1]
            try:
                await insert_db(message.author, handle)
                await self.give_role(message.author, handle)
            except Exception as e:
                print(f'Exception {e}: {e.args}')

    async def give_role(self, member, handle):
        rank = cf_api.get_codeforces_user_maxRank([handle])[handle]["maxRank"]
        rank = rank.capitalize()
        to_remove = [discord.utils.get(member.guild.roles, name=r) for r in self.roles]
        await member.remove_roles(*to_remove)
        await member.add_roles(discord.utils.get(member.guild.roles, name=rank))

    @tasks.loop(hours=24)
    async def update_roles_daily(self):
        users = HandleDB.select()
        guild = self.client.get_guild(self.brute_guild_id)
        for (name, handle) in users:
            member = guild.get_member_named(name)
            print(member, handle)
            await self.give_role(member, handle)


async def insert_db(member, handle):
    var = cf_api.get_codeforces_user_maxRank([handle])[handle]["maxRank"]
    HandleDB.insert(member.name + "#" + member.discriminator, handle)


def setup(bot):
    bot.add_cog(Handles(bot))

