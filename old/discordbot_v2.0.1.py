# requirements.txtの作るコマンド→ (myenv)$ pip freeze > requirements.txt
import discord
from discord.ext import commands
import random
TOKEN=''
VERSION='v2.0.1'

# 接続に必要なオブジェクトを生成
description = '''BさんのBBBot (v2.0.1)'''

# bot = discord.Client()
# bot = commands.Bot(command_prefix='?', description=description)
bot = commands.Bot(command_prefix='?')

# 起動時に動作する処理
@bot.event
async def on_ready():
    # ログイン通知
    # await greet('BBBotが起動したよ！')
    print(bot.user.name + ' is logged in.')
    # https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.change_presence
    # https://discordpy.readthedocs.io/en/latest/api.html#discord.BaseActivity
    # await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="B is bot"))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="B is Bot "))

# メッセージ受信時に動作する処理
@bot.command()
async def BLOOP(ctx, times: int):
    for i in range(times):
        await message.channel.send('B')
@bot.command()
async def add(ctx, left: int, right: int):
    print(left + right)
    await ctx.send(left + right)

@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.content == '/B!':
        await message.channel.send('B!')
    if message.content == '/B greet':
        await message.channel.send('こんにちは！ BBBot('+VERSION+')だよ．\nよろしくね')
    if message.content == '/B hello':
        await message.channel.send('Hello B!')
    if message.content == '/B help':
        await message.channel.send('/B! : B!で応答します\n /B block : ■と□でBを表現します\n /B greet : 挨拶をします\n /B hello : Hello B!\n /B help : コマンド一覧を表示します')
        # await message.channel.send('/B! : B!で応答します\n /B block : ■と□でBを表現します\n /B greet : 挨拶をします\n /B hello : Hello B!\n /B help : コマンド一覧を表示します\n /B melt : :melt:\n /B abya : :abya:')
    if message.content == '/B block':
        await message.channel.send('□□□□□□□□\n□■■■■□□□\n□■□□□■□□\n□■□□□■□□\n□■■■■□□□\n□■□□□■□□\n□■□□□□■□\n□■□□□□■□\n□■■■■■□□\n□□□□□□□□')
    # if '知らんけど（画像略' in message.content:
    #     filepath = 'https://pbs.twimg.com/media/DoGwbj0UwAALenI.jpg'
    #     await message.channel.send(file=discord.File(filepath)
    # if message.content == '/B melt':
    #     filepath = 'https://dic.nicovideo.jp/oekaki/674964.png'
    #     await message.channel.send_file(filepath)
    # if message.content == '/B abya':
    #     filepath = 'https://livedoor.blogimg.jp/mn726/imgs/0/3/03812153.jpg'
    #     await message.channel.send_file(filepath)

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)