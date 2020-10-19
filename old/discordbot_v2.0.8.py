# requirements.txtの作るコマンド→ (myenv)$ pip freeze > requirements.txt
from __future__ import unicode_literals

import io
import aiohttp #画像転送系
# import requests #req
import urllib.request
import urllib.parse
import json
import discord
from discord.ext import commands
import random
import youtube_dl

TOKEN=''
A3RT_KEY=''
VERSION='v2.0.8'

# 接続に必要なオブジェクトを生成
description = '''BさんのBBBot (v2.0.8)'''

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
class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='足し算')
    async def add(self, ctx, left: str, right: str):
        """Add number + number"""
        left = float(left); right = float(right)
        await ctx.send(left + right)
    @commands.command(description='引き算')
    async def sub(self, ctx, left: str, right: str):
        """Sub number - number"""
        left = float(left); right = float(right)
        await ctx.send(left - right)
    @commands.command(description='掛け算')
    async def mul(self, ctx, left: str, right: str):
        """Mul number * number"""
        left = float(left); right = float(right)
        await ctx.send(left * right)
    @commands.command(description='割り算')
    async def div(self, ctx, left: str, right: str):
        """Div number / number"""
        left = float(left); right = float(right)
        await ctx.send(left / right)
#---------------------------------------------------------- B系
class B(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='Bを連続送信します')
    async def BLOOP(self, ctx, times: int):
        """BLOOP number<=11"""
        if times > 12 :
            await ctx.send('too B!');
            return
        for i in range(times):
            await ctx.send('B')
    @commands.command(description='greet, hello, help, block')
    async def B(self, ctx, swit: str):
        """B + (greet, hello, block)"""
        if swit == 'greet':
            await ctx.send('こんにちは！ BBBot('+VERSION+')だよ。\nよろしくね')
        elif swit == 'hello':
            await ctx.send('Hello B!')
        # elif swit == 'help':
        #     await ctx.send('?add, ?sub, ?mul, ?div : 計算\n?BLOOP n : Bを連続送信します\n?B greet, hello, help, block : あいさつ, Hello B!, ヘルプ, □と■のB')
        elif swit == 'block':
            await ctx.send('□□□□□□□□\n□■■■■□□□\n□■□□□■□□\n□■□□□■□□\n□■■■■□□□\n□■□□□■□□\n□■□□□□■□\n□■□□□□■□\n□■■■■■□□\n□□□□□□□□')
        elif swit == 'is GOD':
            await ctx.send('B IS GOD!')
        elif swit == 'is CAT':
            await get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/733937061199085610/766527935377047552/neko.png', 'uchuu_neko.png')
        elif swit == 'is DOG':
            await get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/705099416083890281/767549816862539846/camera_dog.png', 'camera_dog.png')
        elif swit == 'is POT':
            await ctx.send('https://www.google.com/teapot')
        else:
            await ctx.send('B!')
#----------------------------------------------------------画像系
class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='melt picture')
    async def melt(self, ctx):
        """melt picture"""
        await get_pic(self, ctx, 'https://dic.nicovideo.jp/oekaki/674964.png', 'melt.png')
    @commands.command(description='abya picture')
    async def abya(self, ctx):
        """abya picture"""
        await get_pic(self, ctx, 'https://livedoor.blogimg.jp/mn726/imgs/0/3/03812153.jpg', 'abya.png')
    @commands.command(description='shiran kedo~ picture')
    async def shiran(self, ctx):
        """shiran kedo~ picture"""
        await get_pic(self, ctx, 'https://pbs.twimg.com/media/DoGwbj0UwAALenI.jpg', 'shiran.jpg')
    @commands.command(description='party parrot GIF')
    async def party(self, ctx):
        """party parrot GIF"""
        await get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/705099416083890281/766528750456012841/parrot.gif', 'party_parrot.gif')
    @commands.command(description='B picture')
    async def b_pic(self, ctx):
        """B picture"""
        await get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/705099416083890281/766668684188975114/letter-b-clipart-158558-5546542.jpg', 'b_picture')


    @commands.command(description='send photo')
    async def b_img(self, ctx, url: str, file_name: str):
        """b_img url file_name"""
        await get_pic(self, ctx, url, file_name)

async def get_pic(self, ctx, url: str, file_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send('server error... b')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, file_name))
#----------------------------------------------------------AI系
class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='a3rt AI TalkAPI')
    async def ai(self, ctx, talk: str):
        """a3rt AI TalkAPI"""
        data = urllib.parse.urlencode({"apikey":A3RT_KEY, "query":talk}).encode('utf-8')
        request = urllib.request.Request('https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk', data)
        res = urllib.request.urlopen(request)
        json_load = json.load(res)
        # await ctx.send('精度:'+str(json_load['results'][0]['perplexity'])+"\n"+json_load['results'][0]['reply'])
        await ctx.send(json_load['results'][0]['reply'])
#----------------------------------------------------------youtube-dl
class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='youtube-dl')
    async def ydl_m(self, ctx, url: str):
        """youtube-dl url : DL best quority audio. [max 8MB]"""
        ydl_opts={
            'format':'bestaudio/best'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            # data = io.BytesIO(await ydl.download([url]))
            # await ctx.send(file=discord.File(data))

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
bot.add_cog(Calc(bot))
bot.add_cog(B(bot))
bot.add_cog(Image(bot))
bot.add_cog(AI(bot))
bot.add_cog(youtube(bot))
bot.run(TOKEN)
