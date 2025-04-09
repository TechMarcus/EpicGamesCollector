import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTM1MDg2NjA3ODQwNTg5MDE3OQ.GK6sRG.Ie3OhtuXim1A74QZosSTK-eJR8qxiPEyqWeMqA')
