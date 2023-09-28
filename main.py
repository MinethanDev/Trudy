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
    'vm' : {'titre': "I became the villains mother", 'chapitre': "Non programmé", 'date': "Non programmé", 'image': "https://i.imgur.com/mLDfvZG.png", 'image_released': "https://i.imgur.com/qqrGUgv.png", 'roleid': "1024373574716362783"},
    'ch' : {'titre': "I am the child of this house", 'chapitre': "Non programmé", 'date': "Non programmé", 'image': "https://i.imgur.com/HVZkrWC.png", 'image_released': "https://i.imgur.com/h5koncP.png", 'roleid': "904762282968481802"}
}

# Initialisation du bot
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="lire des webtoons"))
    print("Trudy a correctement démarrée et est connectée à Discord.")

# Commande /programmer
@bot.tree.command(name="programmer", description="Programmer la sortie d'un prochain chapitre")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str], chapitre: str, date: str):
    release_chap[serie.value]['chapitre'] = chapitre
    release_chap[serie.value]['date'] = date
    await interaction.response.send_message("{0}\nTu viens de programmer le chapitre **{1}** de la série **{2}** au **{3}** !".format('<@' + str(interaction.user.id) + '>', chapitre, release_chap[serie.value]['titre'], date))
    print("{0} a programmé le chapitre {1} de la série {2} au {3}".format(interaction.user, release_chap[serie.value]['chapitre'], release_chap[serie.value]['titre'], date))

# Commande /sortie
@bot.tree.command(name="sortie", description="Savoir quand est prévue la prochaine sortie d'une série !")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str]):
    if release_chap[serie.value]['date'] != "Non programmé":
        embed = discord.Embed(
            title="Prochaine Sortie !",
            description="Sortie du prochain chapitre de {0}".format(release_chap[serie.value]['titre']),
            color=discord.Color.blue()
        )
        embed.set_image(url=release_chap[serie.value]['image'])
        embed.add_field(name="Chapitre", value=release_chap[serie.value]['chapitre'], inline=False)
        embed.add_field(name="Date de sortie", value=release_chap[serie.value]['date'], inline=False)
    else:
        embed = discord.Embed(
            title="Aïe aïe aïe...",
            description="La date de sortie du prochain chapitre de **{0}** n'a pas été programmée...".format(release_chap[serie.value]['titre']),
            color=discord.Color.red()
        )
    embed.set_author(name="Trudy", icon_url="https://i.imgur.com/X3LwsLZ.jpg")
    await interaction.response.send_message('{0}'.format('<@' + str(interaction.user.id) + '>'), embed=embed)

# Commande /annonce
@bot.tree.command(name="annonce", description="Envoyer une annonce des sorties du jour")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    app_commands.Choice(name="Toutes", value="all")
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str]):
    embed = discord.Embed(
        title="Nouvelles sorties !",
        description="Les sorties du jour Traducfr1, la traduction pour tous",
        color=discord.Color.blue()
    )
    embed.set_author(name="Trudy", icon_url="https://i.imgur.com/X3LwsLZ.jpg")
    if serie.value != "all":
        embed.set_image(url=release_chap[serie.value]['image_released'])
        embed.add_field(name=release_chap[serie.value]["titre"], value=f"Chapitre {release_chap[serie.value]['chapitre']}", inline=False)
        embed.add_field(name="Mention", value="<@&"+ release_chap[serie.value]["roleid"] + ">", inline=False)
    else:
        embed.set_image(url="https://i.imgur.com/EX7ithU.png")
        embed.add_field(name="I became the villains mother", value=f"Chapitre {release_chap['vm']['chapitre']}", inline=False)
        embed.add_field(name="I am the child of this house", value=f"Chapitre {release_chap['ch']['chapitre']}", inline=False)
        embed.add_field(name="Mentions", value="{0}\n{1}".format("<@&"+ release_chap["vm"]["roleid"] + ">", "<@&"+ release_chap["ch"]["roleid"] + ">"), inline=False)
    await interaction.response.send_message(embed=embed)
    print("{0} a annoncé la sortie du prochain chapitre de {1}".format(interaction.user, serie.value))

# Commande /deprogrammer
@bot.tree.command(name="deprogrammer", description="Annuler la sortie d'un chapitre")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch")
    ])
async def deprogrammer(interaction: discord.Interaction, serie: app_commands.Choice[str]):
    release_chap[serie.value]['chapitre'] = "Non programmé"
    release_chap[serie.value]['date'] = "Non programmé"
    await interaction.response.send_message("{0}\nTu viens de déprogrammer le prochain chapitre de **{1}**".format('<@' + str(interaction.user.id) + '>', release_chap[serie.value]['titre']))
    print("{0} a déprogrammé la sortie du prochain chapitre de {1}".format(interaction.user, release_chap[serie.value]['titre']))

# Exécution du bot
bot.run()
