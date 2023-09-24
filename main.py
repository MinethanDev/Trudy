# Importations bibliothèques
import discord
from discord import app_commands
from discord.ext import commands

# Déclaration du bot & du client
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

# Stockage release
vm_chapitre = ""
vm_date = ""
ch_chapitre = ""
ch_date = ""

# Initialisation du bot
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="lire des webtoons"))
    print("Trudy a correctement démarrée et est connectée à Discord.")

# Commande /programmation
@bot.tree.command(name="programmer", description="Programmer la sortie d'un prochain chapitre")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str], chapitre: str, date: str):
    if (serie.value == 'vm'):
        global vm_chapitre, vm_date
        vm_chapitre = chapitre
        vm_date = date

        print("{0} a programmé le chapitre {1} de la série {2} au {3}".format('<@' + str(interaction.user.id) + '>', chapitre, serie, date))
        await interaction.response.send_message("{0}\nTu viens de programmer le chapitre **{1}** de la série **I became the villains mother** au **{2}** !".format('<@' + str(interaction.user.id) + '>', chapitre, date))
        
    elif (serie.value == 'ch'):
        global ch_chapitre, ch_date
        ch_chapitre = chapitre
        ch_date = date
        print("{0} a programmé le chapitre {1} de la série {2} au {3}".format('<@' + str(interaction.user.id) + '>', chapitre, serie, date))
        await interaction.response.send_message("{0}\nTu viens de programmer le chapitre **{1}** de la série **I am the child of this house** au **{2}** !".format('<@' + str(interaction.user.id) + '>', chapitre, date))

# Commande /sortie
@bot.tree.command(name="sortie", description="Savoir quand est prévue la prochaine sortie d'une série !")
@app_commands.choices(serie=[
    app_commands.Choice(name="I became the villains mother", value="vm"),
    app_commands.Choice(name="I am the child of this house", value="ch"),
    ])
async def sortie(interaction: discord.Interaction, serie: app_commands.Choice[str]):
    if (serie.value == 'vm'):
        await interaction.response.send_message("{0}\nLa prochaine sortie pour **I became the villains mother** est celle du chapitre **{1}** !\nElle est prévue au **{2}** !".format('<@' + str(interaction.user.id) + '>', vm_chapitre, vm_date))
    elif (serie.value == 'ch'):
        await interaction.response.send_message("{0}\nLa prochaine sortie pour **I am the child of this house** est celle du chapitre **{1}** !\nElle est prévue au **{2}** !".format('<@' + str(interaction.user.id) + '>', ch_chapitre, ch_date))

# Exécution du bot
bot.run()
