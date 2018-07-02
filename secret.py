import discord
import asyncio
import requests
import random
import string
from discord.ext import commands
from discord.ext.commands import Bot
bot = commands.Bot(command_prefix = '+')

bot.ver_Count = 1
bot.code_count = 1
bot.v_users = []
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='+helpverify'), status=discord.Status('online'),afk=False)

def random_generator(size=8, chars=string.ascii_uppercase + string.digits):
    class_code = '+Verify_Code'
    return class_code + ''.join(random.choice(chars) for x in range(size))

@bot.command(pass_context=True)
async def helpverify(ctx):
    embed = discord.Embed(title = "How to verify:", description='', color=0x00ff00 )
    embed.add_field(name="Step1:", value='Ask the bot for a random code by using the command "+send_code", The bot will DM you the code'+
        'The code is valid for any server you are in. ', inline=False)
    embed.add_field(name="Step2:", value='Copy the code and go on your brickplanet account setting', inline=False)
    embed.add_field(name="Step3:", value='Insert the code in your profile blurd ', inline=False)
    embed.add_field(name="Step4:", value='Go on the server you want to verify your self and say +verify <UserName>', inline=False)
    embed,set_footer(text='For any bugs problems blame GreekSymbol#4686, in other words DM GreekSymbol#4686 and report it')    
    await bot.send_message(ctx.message.author, embed=embed)

##############################
@bot.command(pass_context=True)
async def send_code(ctx):
    global code_sent
    code_sent = random_generator()
    global code_for_user
    code_for_user = ctx.message.author
    await bot.send_message(ctx.message.author, "Hello {} This is your verification code: ".format(ctx.message.author) +  "**"+code_sent+"**" + "  _For verification help say -helpverify_")
    await bot.send_message(ctx.message.channel, '{0.author.mention}'.format(ctx.message) + " Sliding into  your DMs :thumbsup:")
    bot.code_count = bot.code_count + 1



##################################
@bot.command(pass_context=True)
async def verify(ctx, user):
    try:
      r = requests.get("https://www.brickplanet.com/web-api/users/get-user/"+user)
      data = r.json()
      blurb = data['About']
      if code_sent in blurb:
          print("Code was found in the blurb!!")
          server = ctx.message.server
          role = discord.utils.get(server.roles, name="Verified")
          await bot.add_roles(ctx.message.author, role)
          await bot.change_nickname(ctx.message.author , nickname = data['Username'])
          await bot.delete_message(ctx.message)
          await bot.send_message(ctx.message.channel, '{0.author.mention}'.format(ctx.message) + "Verified!")
      else:
          await bot.delete_message(ctx.message)
          await bot.send_message(ctx.message.channel, '{0.author.mention}'.format(ctx.message) + 'Code not found in blurb')
    except discord.Forbidden:
        await bot.send_message(ctx.message.channel, '{0.author.mention}'.format(ctx.message) + 'Can not edit your information..You are too tall for me to reach')
bot.run(TOEKN)
