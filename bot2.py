import discord
import responses

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class EvaDiscordBot(commands.Bot):
    def __int__(self):
        super().__init__()

    async def on_ready(self):
        print(f'{self.user.display_name} est en marche !')

    async def on_message(self, message):
        response = responses.handle_response(message.content.lower())

        if message.author == self.user:
            return

        if response is not None:
            await message.channel.send(response)

    async def on_member_join(self, member):
        bienvenue_channel: discord.TextChannel = self.get_channel(1085268089257607278)
        await bienvenue_channel.send(content=f"Ravi de te voir parmi nous {member.display_name}")
        role = discord.utils.get(member.guild.roles, name='Recrue')
        await member.add_roles(role)

    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.guilds)

            if payload.emoji.name == '🎮':
                role = discord.utils.get(guild.roles, name='Gaming')
            elif payload.emoji.name == '🦆':
                role = discord.utils.get(guild.roles, name='🦆Canard')
            else:
                role = None

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)

    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.guilds)

            if payload.emoji.name == '🎮':
                role = discord.utils.get(guild.roles, name='Gaming')
            elif payload.emoji.name == '🦆':
                role = discord.utils.get(guild.roles, name='🦆Canard')
            else:
                role = None

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
