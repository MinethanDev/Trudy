# Importations bibliothèques
import discord
from discord import app_commands
from discord.ext import commands

# Déclaration du bot & du client
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

# Stockage release
release_chap = {
    'vm' : {'titre': "I became the villains mother", 'chapitre': "", 'date': "", 'image': "https://i.imgur.com/mLDfvZG.png  "},
    'ch' : {'titre': "I am the child of this house", 'chapitre': "", 'date': "", 'image': "https://i.imgur.com/ji6brr1.png"}
}

# Initialisation du bot
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="lire des webtoons"))
    print("Trudy a correctement démarrée et est connectée à Discord.")

# Commande /programmation
@bot.tree.command(name="programmer", description="Programmer la sortie d'un prochain chapitre")
@commands.has_permissions(administrator=True)
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str], chapitre: str, date: str):
        release_chap[serie.value]['chapitre'] = chapitre
        release_chap[serie.value]['date'] = date
        print("{0} a programmé le chapitre {1} de la série {2} au {3}".format('<@' + str(interaction.user.id) + '>', chapitre, serie, date))
        await interaction.response.send_message("{0}\nTu viens de programmer le chapitre **{1}** de la série **{2}** au **{3}** !".format('<@' + str(interaction.user.id) + '>', chapitre, release_chap[serie.value]['titre'], date))

# Commande /sortie
@bot.tree.command(name="sortie", description="Savoir quand est prévue la prochaine sortie d'une série !")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str]):
        embed = discord.Embed(
            title="Prochaine Sortie !",
            description="Sortie du prochain chapitre de {0}".format(release_chap[serie.value]['titre']),
            color=discord.Color.blue()
        )
        embed.add_field(name="Chapitre", value=release_chap[serie.value]['chapitre'], inline=False)
        embed.add_field(name="Date de sortie", value=release_chap[serie.value]['date'], inline=False)
        embed.set_author(name="Trudy", icon_url="https://i.imgur.com/X3LwsLZ.jpg")
        embed.set_image(url=release_chap[serie.value]['image'])
        await interaction.response.send_message('{0}'.format('<@' + str(interaction.user.id) + '>'), embed=embed)

# Exécution du bot
bot.run()
