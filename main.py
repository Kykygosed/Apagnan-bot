from keep_alive import keep_alive  # Importer le fichier keep_alive

keep_alive()  # Garder le bot en vie
import discord
from discord.ext import commands, tasks
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

reponses_speciales = {
    "yo": "Salutations 🫡",
    "ça va ?": "Oui et toi ? 😊",
    "bien": "Super ! ☺️",
    "merci apagnan": "De rien ! ☺️",
    "j'ai besoin d'aide": "Tu peux demander à Apagnan, il est très sympa 😊",
    "fdp": "Évite d'insulter, l'administrateur va te sanctionner ⚠️",
    "quoi": "feur",
    "quoi?": "feur",
    "hein" : "apagnan",
    "hein?" : "apagnan",
    "&testapagnan" : "Mes programmes sont opérationels!"
}

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def envoyer(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def msg(ctx, utilisateur: discord.User, *, message: str):
    # Envoi du message en MP à l'utilisateur
    await utilisateur.send(message)
    await ctx.send(f"Message envoyé à {utilisateur.name}!")

# Commande !ban avec durée
@bot.command()
@commands.has_permissions(ban_members=True)  # Vérifie si l'utilisateur a la permission d'administrateur
async def ban(ctx, member: discord.Member, reason: str, duration: str):
    # Vérifier le format de la durée (m, h, j)
    time_units = {'m': 60, 'h': 3600, 'j': 86400}  # minutes, heures, jours
    try:
        # Extraire le nombre et l'unité de la durée
        number = int(duration[:-1])  # Extraire le nombre (ex : "1" de "1m")
        unit = duration[-1]  # Extraire l'unité (ex : "m" de "1m")
        
        if unit not in time_units:
            await ctx.send("Format de durée invalide. Utilisez 'm' pour minutes, 'h' pour heures ou 'j' pour jours.")
            return
        
        # Calculer la durée en secondes
        duration_in_seconds = number * time_units[unit]
        
        # Bannir le membre avec la raison spécifiée
        await member.ban(reason=reason)
        
        # Envoi du message privé au membre banni
        try:
            await member.send(f"Sanction - Kenzo\nVous êtes banni\nRaison : {reason}\nDurée : {duration}\nOu ferez attention la prochaine fois!")
        except discord.Forbidden:
            await ctx.send(f"Impossible d'envoyer un message privé à {member.name}. Il pourrait avoir les MP fermés.")
        
        await ctx.send(f"{member.mention} a été banni pour {duration} en raison de : {reason}")
        
        # Attendre pendant la durée spécifiée
        await asyncio.sleep(duration_in_seconds)
        
        # Débannir le membre après la durée
        await member.unban(reason="Bannissement temporaire terminé.")
        await ctx.send(f"{member.mention} a été débanni après {duration}.")

    except ValueError:
        await ctx.send("La durée spécifiée est invalide. Exemple : `1m`, `2h`, `3j`.")
    except Exception as e:
        await ctx.send(f"Une erreur est survenue : {e}")

# Commande !lock pour verrouiller le salon avec slowmode
@bot.command()
@commands.has_permissions(manage_channels=True)  # Vérifie si l'utilisateur a la permission de gérer les salons
async def lock(ctx):
    # Appliquer un slowmode de 10 secondes (ajuste la durée selon ton besoin)
    await ctx.channel.edit(slowmode_delay=10)
    await ctx.send(f"Le salon {ctx.channel.mention} a été verrouillé (mode lent activé). Les messages seront envoyés avec un délai de 10 secondes.")

# Commande !unlock pour déverrouiller le salon
@bot.command()
@commands.has_permissions(manage_channels=True)  # Vérifie si l'utilisateur a la permission de gérer les salons
async def unlock(ctx):
    # Supprimer le slowmode (mettre à 0)
    await ctx.channel.edit(slowmode_delay=0)
    await ctx.send(f"Le salon {ctx.channel.mention} a été déverrouillé (mode lent désactivé). Les messages peuvent être envoyés sans délai.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message reçu: {message.content}")  # Debug, affiche tous les messages

    # Traite d'abord les commandes
    await bot.process_commands(message)

    contenu = message.content.lower()
    if contenu in reponses_speciales:
        await message.channel.send(reponses_speciales[contenu])

# Lancement du bot avec ton token
bot.run(os.getenv("DISCORD_TOKEN"))
