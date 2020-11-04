import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
REACTION_CHANNEL = os.getenv('REACTION_CHANNEL')
MESSAGE_ID = int(os.getenv('REACTION_MESSAGE_ID'))

# I notice most people tend to use custom emoji tied to roles
# that way they can just use the emoji name as the role name
# that allows for new roles and emjoi to be created dynamically
# but it also feels a bit brittle to me and relies on custom emoji
# far better in my mind to have to have it human configured
role_map = {
    '🥚' : 'Destiny',
    '🛳️' : 'Sea of Friends',
    '🔪' : 'Among Us',
    '💯' : 'The Living Embodiment Of The 100 Emoji'} # an emoji that connects to a non-role for testing purposes

# we need member intents for role assignment to work
# this is because discord otherwise won't give use the data needed to identify WHO is reacting to things
# also need to make sure that the bot is configured to have these permission on the discord API side
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# I wanted to do this using the built in discord.py bot commands
# but I think I have to completely overhaul the structure to do so
# I THINK that by setting this up as client it can't also be a bot
# but a bot can be a client, will have to explore this later on
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if client.user not in message.mentions:
        return

    if "shutdown please" in message.content.lower():
        # is the person messaging the bot an admin?
        if any(r for r in message.author.roles if r.name == "Admin"):
            print("an admin sent the shutdown message")
            await message.channel.send('Toodles')
            await client.close()
        else:
            await message.channel.send("Sorry, you're not authorised to kill me")
        return

# not entirely sure why, but the message cache seems really small
# so instead of being able to use the nice convenience methods
# we find ourselves using the raw forms, which work fine I guess
# just need to do a bit more unwrapping of the payload first
@client.event
async def on_raw_reaction_remove(payload):
    channel = discord.utils.get(client.get_all_channels(), id=payload.channel_id)
    if channel is None:
        print("Unable to locate the channel")
        return

    if channel.name != REACTION_CHANNEL:
        print("Reaction is in a channel we don't care about")
        return
    
    if payload.message_id != MESSAGE_ID:
        print(f"Reaction is to a message we don't care about: {payload.message_id} vs {MESSAGE_ID}")
        return
    
    guild = discord.utils.get(client.guilds, id=payload.guild_id)
    if guild is None:
        print("Unable to identify the server, this should be impossible to have found the channel but not the guild...")
        return

    # some times there is a member in the payload, not always though because of discord API rules
    # whatever...
    member = payload.member if payload.member != None else guild.get_member(payload.user_id)

    if member is None:
        print(f"Unable to identify the member {payload.user_id} who posted the reaction")
        return
    
    if payload.emoji.name is None:
        print(f"Unable to identify the emoji {payload.emoji}")
        return
    
    role_name = role_map.get(payload.emoji.name)
    if role_name is None:
        print("unrecognised role")
        #await channel.send(f"That dashing looking blob {member.nick} removed their invalid role emoji, well done blob.")
        return
    
    role = discord.utils.get(guild.roles, name = role_name)
    if role is None:
        print(f"unable to identify the role {role_name}")
        return
    
    await member.remove_roles(role)
    print(f"removed {role.name} from {member.nick}")

@client.event
async def on_raw_reaction_add(payload):

    channel = discord.utils.get(client.get_all_channels(), id=payload.channel_id)
    if channel is None:
        print("Unable to locate the channel")
        return

    if channel.name != REACTION_CHANNEL:
        print("Reaction is in a channel we don't care about")
        return
    
    if payload.message_id != MESSAGE_ID:
        print(f"Reaction is to a message we don't care about: {payload.message_id} vs {MESSAGE_ID}")
        return
    
    guild = discord.utils.get(client.guilds, id=payload.guild_id)
    if guild is None:
        print("Unable to identify the server, this should be impossible to have found the channel but not the guild...")
        return

    # some times there is a member in the payload, not always though because of discord API rules
    # whatever...
    member = payload.member if payload.member != None else guild.get_member(payload.user_id)

    if member is None:
        print(f"Unable to identify the member {payload.user_id} who posted the reaction")
        return
    
    if payload.emoji.name is None:
        print(f"Unable to identify the emoji {payload.emoji}")
        #await channel.send(f"Hey {member.nick}, you reacted with an emoji but I cannot identify it, sorry. Don't blame me, blame my programmer")
        return
    
    role_name = role_map.get(payload.emoji.name)
    if role_name is None:
        print(f"unrecognised role {payload.emoji.name}")
        #await channel.send(f"That Fool Of A Took {member.nick}™ reacted with an invalid role emoji!")
        return
    
    role = discord.utils.get(guild.roles, name = role_name)
    if role is None:
        print(f"unable to identify the role {role_name}")
        return
    
    await member.add_roles(role)
    print(f"added {role.name} to {member.nick}")

client.run(TOKEN)