import os
import discord
from notebooks import cf_api
from notebooks.DAO import HandleDB
from discord.ext import commands, tasks


class Handles(commands.Cog):
    roles = ["Unrated", "Newbie", "Pupil", "Specialist", "Expert", "Candidate Master", "Grandmaster"]

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
                rank = cf_api.get_codeforces_user_maxRank([handle])[handle]["maxRank"]
                HandleDB.insert(message.author.name + "#" + message.author.discriminator, handle)
                await self.give_role(message.author, rank)
                await message.add_reaction('✅')
            except Exception as e:
                await message.add_reaction('❌')
                print(f'Exception {e}: {e.args}')

    async def give_role(self, member, rank):
        rank = rank.capitalize()
        to_remove = [discord.utils.get(member.guild.roles, name=r) for r in self.roles]
        await member.remove_roles(*to_remove)
        await member.add_roles(discord.utils.get(member.guild.roles, name=rank))

    @tasks.loop(hours=1)
    async def update_roles_daily(self):
        users = HandleDB.select_all()
        ranks = cf_api.get_codeforces_user_maxRank([v[1] for v in users])
        guild = self.client.get_guild(int(os.environ["GUILD_ID"]))
        for (name, handle) in users:
            member = guild.get_member_named(name)
            if member is not None:
                rank = ranks[handle]["maxRank"]
                await self.give_role(member, rank)
            else:
                print(f"{name} not found")


def setup(bot):
    bot.add_cog(Handles(bot))
