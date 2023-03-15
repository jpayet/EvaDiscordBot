import os
import discord
import responses

from dotenv import load_dotenv
load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} est lancé !')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} a dit : '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    @client.event
    async def on_member_join(member):
        bienvenue_channel: discord.TextChannel = client.get_channel(1085268089257607278)
        await bienvenue_channel.send(content=f"Ravi de te voir parmi nous {member.display_name}")
        role = discord.utils.get(member.guild.roles, name='Recrue')
        await member.add_roles(role)

    @client.event
    async def on_raw_reaction_add(payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            if payload.emoji.name == '🎮':
                role = discord.utils.get(guild.roles, name='Gaming')
            if payload.emoji.name == '🦆':
                role = discord.utils.get(guild.roles, name='🦆Canard')
            else:
                pass


            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                else:
                    print("Member not found")
            else:
                print("Role not found")

    @client.event
    async def on_raw_reaction_remove(payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            if payload.emoji.name == '🎮':
                role = discord.utils.get(guild.roles, name='Gaming')
            if payload.emoji.name == '🦆':
                role = discord.utils.get(guild.roles, name='🦆Canard')
            else:
                pass

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                else:
                    print("Member not found")
            else:
                print("Role not found")

    client.run(os.getenv("TOKEN"))
