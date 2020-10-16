# requirements.txtの作るコマンド→ (myenv)$ pip freeze > requirements.txt
import io
import aiohttp #画像転送系
import discord
from discord.ext import commands
import random
TOKEN=''
VERSION='v2.0.2'

# 接続に必要なオブジェクトを生成
description = '''BさんのBBBot (v2.0.2)'''

# bot = discord.Client()
bot = commands.Bot(command_prefix='?', description=description)

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
#---------------------------------------------------------- 計算系
@bot.command(description='足し算')
async def add(ctx, left: int, right: int):
    """Add"""
    await ctx.send(left + right)
@bot.command(description='引き算')
async def sub(ctx, left: int, right: int):
    """Sub"""
    await ctx.send(left - right)
@bot.command(description='掛け算')
async def mul(ctx, left: int, right: int):
    """Mul"""
    await ctx.send(left * right)
@bot.command(description='割り算')
async def div(ctx, left: int, right: int):
    """Div"""
    await ctx.send(left / right)
#---------------------------------------------------------- B系
@bot.command(description='Bを連続送信します')
async def BLOOP(ctx, times: int):
    """B LOOP"""
    if times > 12 :
        await ctx.send('too B!');
        return
    for i in range(times):
        await ctx.send('B')
@bot.command(description='greet, hello, help, block')
async def B(ctx, swit: str):
    """B Hello!"""
    if swit == 'greet':
        await ctx.send('こんにちは！ BBBot('+VERSION+')だよ。\nよろしくね')
    elif swit == 'hello':
        await ctx.send('Hello B!')
    elif swit == 'help':
        await ctx.send('?add, ?sub, ?mul, ?div : 計算\n ?BLOOP n : Bを連続送信します\n ?B greet, hello, help, block : あいさつ, Hello B!, ヘルプ, □と■のB')
    elif swit == 'block':
        await ctx.send('□□□□□□□□\n□■■■■□□□\n□■□□□■□□\n□■□□□■□□\n□■■■■□□□\n□■□□□■□□\n□■□□□□■□\n□■□□□□■□\n□■■■■■□□\n□□□□□□□□')
    else:
        await ctx.send('B!')
#----------------------------------------------------------画像系
@bot.command(description='original melt')
async with aiohttp.ClientSession() as session:
    async with session.get('https://dic.nicovideo.jp/oekaki/674964.png') as resp:
        if resp.status != 200:
            return await channel.send('server error... b')
        data = io.BytesIO(await resp.read())
        await channel.send(file=discord.File(data, 'melt.png'))
# @bot.event
# async def on_message(message):
#     # メッセージ送信者がBotだった場合は無視する
#     if message.author.bot:
#         return
#     if message.content == '/B!':
#         await message.channel.send('B!')
#     if message.content == '/B greet':
#         await message.channel.send('こんにちは！ BBBot('+VERSION+')だよ．\nよろしくね')
#     if message.content == '/B hello':
#         await message.channel.send('Hello B!')
#     if message.content == '/B help':
#         await message.channel.send('/B! : B!で応答します\n /B block : ■と□でBを表現します\n /B greet : 挨拶をします\n /B hello : Hello B!\n /B help : コマンド一覧を表示します')
#         # await message.channel.send('/B! : B!で応答します\n /B block : ■と□でBを表現します\n /B greet : 挨拶をします\n /B hello : Hello B!\n /B help : コマンド一覧を表示します\n /B melt : :melt:\n /B abya : :abya:')
#     if message.content == '/B block':
#         await message.channel.send('□□□□□□□□\n□■■■■□□□\n□■□□□■□□\n□■□□□■□□\n□■■■■□□□\n□■□□□■□□\n□■□□□□■□\n□■□□□□■□\n□■■■■■□□\n□□□□□□□□')
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
