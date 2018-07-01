import discord
import asyncio
import requests
import random
import string
import os 
from discord.ext import commands
from discord.ext.commands import Bot
bot = commands.Bot(command_prefix = '+')

bot.ver_Count = 1
bot.code_count = 1
bot.v_users = []

TOKEN=os.environ['BOT_TOKEN']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_server_join(server):
    await bot.create_role(server,name="Verified")
def random_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
############################Sends the user a random code####################################
@bot.command(pass_context=True)
async def send_code(ctx):
    global code_sent
    code_sent = random_generator()
    global code_for_user
    code_for_user = ctx.message.author
    await bot.send_message(ctx.message.author, "Hello {} This is your verification code: ".format(ctx.message.author) +  "**"+code_sent+"**" + "  _For verification help say -helpverify_")
    await bot.send_message(ctx.message.channel, '{0.author.mention}'.format(ctx.message) + " Sliding into  your DMs :thumbsup:")
    bot.code_count = bot.code_count + 1

@bot.command(pass_context=True)
async def helpverify(ctx):
    embed = discord.Embed(title = "How to verify:", description='', color=0x00ff00 )
    embed.add_field(name="Step1:", value='Ask the bot for a random code by using the command "+send_code", The bot will DM you the code'+
        'The code is valid for any server you are in. ', inline=False)
    embed.add_field(name='Step2', value='Go on brickplanet.com and login(*if you dont have an account sign up*)', inline=False)
    embed.add_field(name='Step3', value='Instert the code that bot gave you in your Status', inline=False)
    embed.add_field(name='Step4', value='Go on the server where you want to verify your self, and find the channel to verify your self',inline=False)
    embed.add_field(name='Step5', value='In the channel/server say: +verify <username or userid> <code that was sent by the bot>')

    await bot.send_message(ctx.message.author, embed=embed)



@bot.command(pass_context=True)
async def verify(ctx, user ,code):
    try:
        if ctx.message.author == code_for_user:
            if code == code_sent:
                r = requests.get("https://www.brickplanet.com/web-api/users/get-user/"+user)
                data = r.json()
                if data['Status'] == code:
                    server = ctx.message.server
                    role = discord.utils.get(server.roles, name="Verified")
                    await bot.add_roles(ctx.message.author, role)
                    await bot.change_nickname(ctx.message.author , nickname = data['Username'])
                    await bot.delete_message(ctx.message)
                    await bot.say('Verified!')
                    bot.ver_Count = bot.ver_Count + 1
                    user_fmt = ('**In server: **' +str(ctx.message.server)+ '**User: **' +str(ctx.message.author) + 'Verified account: ' +data['Username'])
                    bot.v_users.append(user_fmt)
                    print(data['Status'])
                else:   
                    await bot.say("Unable to verify user" +'{0.author.mention}'.format(ctx.message))
            else:
                await bot.say('Code is invalid'+'{0.author.mention}'.format(ctx.message))
        else:
            await bot.say('The code is not for you.'+'{0.author.mention}'.format(ctx.message))
    except discord.Forbidden:
        print("Error occured")
        await bot.say("I do have privilege to edit that user's nickname")


##################Logging Info##################

@bot.command(pass_context=True)
@commands.has_role("RANK")
async def get_c_count(ctx):
    await bot.say(bot.code_count)
####################################
@bot.command(pass_context=True)
@commands.has_role("RANK")
async def get_Ver_count(ctx):
    await bot.say(bot.ver_Count)
######################################
@bot.command(pass_context=True)
@commands.has_role("dev_Log_aCess_65")
async def get_Ver_users(ctx):
    user_Em = discord.Embed(title = 'Verified Users', description='list of verified users', color=0x00ff00)
    for i in range(len(bot.v_users)):
        user_Em.add_field(name='User {}'.format(i), value=bot.v_users[i])
    await bot.say(embed=user_Em)
####################################
bot.run(TOKEN)
