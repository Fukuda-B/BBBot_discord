# make requirements.txt command -> (myenv)$ pip freeze > requirements.txt
# Video and audio are file-like objects.

# This Discord bot uses PyNaCl & FFmpeg in VoiceChat class.

# pip update
# powershell: pip install --upgrade ((pip freeze) -replace '==.+','')
# https://www.yukkuriikouze.com/2019/07/12/3105/

# 2.7.0~ | youtube-dl --> yt-dlp

from __future__ import unicode_literals

# ----- basic module ----
import os
import io
import re
import sys
import math
import random
import string
import json
import random
import socket
import time
import platform
import threading
import zipfile
import datetime
import secrets
# ----- extend module -----
import aiohttp
from click import style
from numpy import delete #画像転送系
from pyshorteners import Shortener
from gtts import gTTS
import asyncio
import pathlib
import psutil
import cpuid
# import youtube_dl
import yt_dlp as youtube_dl
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
import urllib.request
import urllib.parse
import ffmpeg
# ---- my module ----
from modules import my_key # get my api keys
from modules import my_music
from modules import brainfuck # my brainfuck interpreter
from modules import kawaii_voice_gtts
from modules import htr # get hattori
from modules import htr_end
from modules import htr_dead
from modules import eq_check
from modules import up_server

VERSION='v2.8.2'

_TOKEN, _A3RT_URI, _A3RT_KEY, _GoogleTranslateAPP_URL,\
    LOG_C, MAIN_C, VOICE_C, HA, _UP_SERVER,\
    M_CALL = my_key.get_keys()

HTR_LIST = htr.get_hattori()
HTRE_LIST = htr_end.end_hattori()
HTRD_LIST = htr_dead.dead_hattori()



description = 'BさんのBBBot ('+VERSION+')'
bot = commands.Bot(
    command_prefix='?', # コマンドの最初の文字
    description=description,
    case_insensitive = True, # コマンドの大文字小文字
)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


#----------------------------------------------------------

# 起動時に動作する処理
@bot.event
async def on_ready():
    # ログイン通知
    print(bot.user.name + ' is logged in.')
    # await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="BBBot "+VERSION, emoji="🍝"))
    # await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="BBBot "+VERSION))

    # await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="B is bot"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="BBBot "+VERSION, emoji="🍝"))
    lChannel = bot.get_channel(LOG_C)
    await lChannel.send('BBBot is Ready! ' + VERSION)

#---------------------------------------------------------- 定期実行系
    # 非同期並行処理
    eqc = eq_check.EqCheck(bot, LOG_C, MAIN_C)
    ups = up_server.UpServer(bot, LOG_C, _UP_SERVER)
    await asyncio.gather(
        eqc.p2peq_check(),
        ups.up_server(),
    )

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    if message.content.startswith('?'):
        lChannel = bot.get_channel(LOG_C)
        await lChannel.send("```"\
            +"\nGuild  : "+str(message.guild.id)\
            +"\nChannel: "+str(message.channel.id)\
            +"\nAuthor : "+str(message.author.name)+"#"\
            +str(message.author.discriminator)\
            +" (ID: "+str(message.author.id)+")"\
            +"\n"+str(message.content)+"```")
        # await lChannel.send("```\n@"+str(message.author.name)+"\n"+str(message.author.id)+"\n"+str(message.content)+" ```")
        if message.author.bot: return # ボットだったら何もしない
        await bot.process_commands(message)

#---------------------------------------------------------- 計算系
class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='計算 Eval')
    # Evalなので攻撃しないでください。
    async def calc(self, ctx, *inc: str):
        """Calc number Eval"""
        inc = ''.join(inc)
        inc = re.sub(r"[\u3000 \t]", "", inc)
        await Basic.send(self, ctx, eval(inc, {}, {'math':math}))

    @commands.command(description='足し算')
    async def add(self, ctx, left: str, right: str):
        """Add number + number"""
        left = float(left); right = float(right)
        await Basic.send(self, ctx, left + right)

    @commands.command(description='引き算')
    async def sub(self, ctx, left: str, right: str):
        """Sub number - number"""
        left = float(left); right = float(right)
        await Basic.send(self, ctx, left - right)

    @commands.command(description='掛け算')
    async def mul(self, ctx, left: str, right: str):
        """Mul number * number"""
        left = float(left); right = float(right)
        await Basic.send(self, ctx, left * right)

    @commands.command(description='割り算')
    async def div(self, ctx, left: str, right: str):
        """Div number / number"""
        left = float(left); right = float(right)
        await Basic.send(self, ctx, left / right)

    @commands.command(description='自己情報量I()')
    async def self_info(self, ctx, p: str):
        """Self-information I(p)"""
        p = float(eval(p, {}, {'math':math}))
        if p == 0.0:
            await Basic.send(self, ctx, 0.0)
        else:
            await Basic.send(self, ctx, -p*math.log2(p))

    @commands.command(description='エントロピー関数計算H()')
    async def ent(self, ctx, p: str):
        """EntropyFunc H(p)"""
        p = float(eval(p, {}, {'math':math}))
        if p == 0.0:
            await Basic.send(self, ctx, 0.0)
        else:
            await Basic.send(self, ctx, -p*math.log2(p)-(1-p)*math.log2(1-p))

    @commands.command(description='乱数(int) 1~x')
    async def rand(self, ctx, p: str):
        """Random(int) 1~x"""
        p = float(eval(p, {}, {'math':math}))
        if p>1:
            await Basic.send(self, ctx, random.randint(1, p))
        else:
            await Basic.send(self, ctx, random.randint(p, 1))

    @commands.command(description='乱数(float)) 1.0~x')
    async def randd(self, ctx, p: str):
        """Random(float) 1.0~x"""
        p = float(eval(p, {}, {'math':math}))
        if p > 1.0:
            await Basic.send(self, ctx, random.uniform(1.0, p))
        else:
            await Basic.send(self, ctx, random.uniform(p, 1.0))

    @commands.command(description='素因数分解(2以上の整数のみ)')
    async def fractor(self, ctx, p: int):
        """Factorization"""
        try:
            p = int(p)
            ct = p
            if p >= 2:
                res = []
                for i in range(2, int(p**0.5)+1):
                    if ct % i == 0:
                        cn = 0
                        while ct % i == 0:
                            ct //= i # intへのキャストの代わり ( /= だとdoubleになってちょっと遅くなるかもしれないので)
                            cn += 1
                        res.append([i, cn])
                if ct != 1: res.append([ct, 1]) # iで割れずに残っている場合
                if res == []: res.append([p, 1]) # 単純に素数の場合
            else:
                await Basic.send(self, ctx, 'The value must be greater than or equal to 2')
            res_t = f'{p} = '
            for i in range(len(res)):
                res_t += f'{res[i][0]}^{res[i][1]}'
                if i != len(res)-1: res_t += ' * '
            await Basic.send(self, ctx, str(res_t))

        except Exception as e:
            print(e)
            await Basic.send(self, ctx, 'The number must be an integer greater than or equal to 2')


#---------------------------------------------------------- B系
class B(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Bを連続送信します')
    async def BLOOP(self, ctx, times: int):
        """BLOOP number<=11"""
        if times > 12 :
            await Basic.send(self, ctx, 'too B!')
            return
        for _ in range(times):
            await Basic.send(self, ctx, 'B')

    @commands.group(description='greet, hello, help, block')
    # async def B(self, ctx, swit: str, swit2: str):
    async def B(self, ctx):
        """B + (greet / sysinfo / hello / block / typing)"""
        if ctx.invoked_subcommand is None:
            await Basic.send(self, ctx, 'B!')

    @B.command()
    async def greet(self, ctx):
        await Basic.send(self, ctx, 'こんにちは！ BBBot('+VERSION+')だよ。\nよろしくね')

    @B.command()
    async def sysinfo(self, ctx):
        ipInfo = 'IP :'+socket.gethostname()+': '+socket.gethostbyname(socket.gethostname())
        platInfo = 'OS : '+platform.platform()
        cpuInfo = 'CPU: '+cpuid.cpu_name()
        #cpuInfo = 'CPU: ['+str(psutil.cpu_count(logical=False))+'C '+str(psutil.cpu_count())+'T]'
        memInfo = 'MEM: '+str('{:.2f}'.format(psutil.virtual_memory().used/(1024*1024)))+'MB / '\
            +str('{:.2f}'.format(psutil.virtual_memory().total/(1024*1024)))+'MB'
        await Basic.send(self, ctx, ipInfo+"\n"+platInfo+"\n"+cpuInfo+"\n"+memInfo)

    @B.command()
    async def hello(self, ctx):
        await Basic.send(self, ctx, 'Hello B!')

    @B.command()
    async def block(self, ctx):
        await Basic.send(self, ctx, '□□□□□□□□\n□■■■■□□□\n□■□□□■□□\n□■□□□■□□\n□■■■■□□□\n□■□□□■□□\n□■□□□□■□\n□■□□□□■□\n□■■■■■□□\n□□□□□□□□')

    @B.command()
    async def ping(self, ctx):
        await Basic.send(self, ctx, f"{bot.latency*1000}ms")

    @B.command()
    async def many_b(self, ctx):
        bbb = ['b']*(1011)
        tx = '```\nThis is 1011B of B (1011).\n'+''.join(bbb)+'```'
        await Basic.send(self, ctx, tx)

    @B.command()
    async def more_b(self, ctx):
        bbb = ['b']*(11*1024)
        tx = 'This is 11KB of B (11*1024).\n'+''.join(bbb)
        await Basic.send(self, ctx, tx)

    @B.command()
    async def most_b(self, ctx):
        bbb = ['b']*(11*1024**2)
        tx = 'This is 11MB of B (11*1024**2).\n'+''.join(bbb)
        await Basic.send(self, ctx, tx)

    @B.command()
    async def typing(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(10)
            ctx.typing()
            await Basic.send(self, ctx, 'B')

    @B.command()
    async def hattori(self, ctx, *tx:str):
        """ htr """
        txx = ' '.join(tx)
        # mChannel = bot.get_channel(MAIN_C)
        if 'end' in txx.lower():
            await Basic.send(self, ctx, HTRE_LIST[random.randrange(len(HTRE_LIST))])
        elif 'd' in txx.lower():
            await Basic.send(self, ctx, HTRD_LIST[random.randrange(len(HTRD_LIST))])
        else:
            await Basic.send(self, ctx, HTR_LIST[random.randrange(len(HTR_LIST))])

    # @B.command()
    # async def morning_call(self, ctx):
    #     """強制モーニングコールが行われる"""
    #     vChannel = bot.get_channel(VOICE_C)
    #     user = bot.fetch_user(HA) # get user from id
    #     await Basic.send(self, ctx, user)
    #     await user.move_to(vChannel)
    #     await vChannel.connect()
    #     VoiceChat.v_music(self, ctx, M_CALL)

    @B.command()
    async def button(self, ctx):
        """B button"""
        buttons = [
                create_button(label="God", custom_id="God", style=ButtonStyle.blue),
                create_button(label="Bot", custom_id="Bot", style=ButtonStyle.green),
                create_button(label="Cat", custom_id="Cat", style=ButtonStyle.red)
        ]
        action_row = create_actionrow(*buttons)
        res = await ctx.send(
            "B is",
            components=[action_row]
        )
        interaction = await wait_for_component(
            bot, components=[action_row]
        )
        # await interaction.edit_origin(content=interaction.component_id)
        await res.delete()
        await Basic.send(self, ctx, f"B is {interaction.component_id}")

#---------------------------------------------------------- 画像系
class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.img_link = {
            # '':{'url':'', 'name':''},
            'melt': {'url':'https://dic.nicovideo.jp/oekaki/674964.png', 'name':'melt.png'},
            'abya': {'url':'https://livedoor.blogimg.jp/mn726/imgs/0/3/03812153.jpg', 'name':'abya.jpg'},
            'shiran': {'url':'https://pbs.twimg.com/media/DoGwbj0UwAALenI.jpg', 'name':'shiran.jpg'},
            'party':{'url':'https://cdn.discordapp.com/attachments/705099416083890281/766528750456012841/parrot.gif', 'name':'party_parrot.gif'},
            'b_pic':{'url':'https://cdn.discordapp.com/attachments/705099416083890281/766668684188975114/letter-b-clipart-158558-5546542.jpg', 'name':'b.jpg'},
            'presen':{'url':'https://cdn.discordapp.com/attachments/733937061199085610/768300192818135040/GPW.gif', 'name':'gaming_presentation.gif'},
            'majiyaba':{'url':'https://pbs.twimg.com/media/C34X4w0UcAEyKW-.jpg', 'name':'majiyaba.jpg'},
            'bohe':{'url':'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/806b36e95d491beec2aaaec7af98ad28-2.gif', 'name':'bohe.gif'},
            'gyu':{'url':'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/58b9f8279c61a217bc7770446a6d542f.gif', 'name':'gyu.gif'},
            'ha':{'url':'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/13a658840a8373deb4355975b3e56e0b.gif', 'name':'ha.gif'},
            'hello':{'url':'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/3f5592cb37efa6b1a0e1f5ac2cc86e26.gif', 'name':'hello.gif'},
            'maken':{'url':'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/a5f64bc592c42aecea1e8fb29eac3642-2.gif', 'name':'maken.gif'},
            'onegai':{'url':'https://maidragon.jp/news/wordpress/wp-content/uploads/2021/07/a533a6932106c9f63ae9ee4ea3a478a5.gif', 'name':'onegai.gif'},
            'b_pet':{'url':'https://cdn.discordapp.com/attachments/705099416083890281/880373964088692736/Pet_the_B.gif', 'name':'Pet_the_B.gif'},
            'thx':{'url':'https://cdn.discordapp.com/attachments/880371118148558848/880701571917307914/meidora2.gif', 'name':'thx.gif'},
        }

    @commands.group(description='send img')
    async def img(self, ctx):
        """send img. melt/abya/shiran/party/... -> ?help img"""
        if ctx.invoked_subcommand is None:
            # await Basic.send(self, ctx, 'img help: `?help img`')
            buttons = []
            actions = [] # action rows
            for i, name in enumerate(self.img_link.keys()):
                buttons.append(create_button(
                    label=name,
                    custom_id=name,
                    style=ButtonStyle.blue
                    ))
                if (i%5==4):
                    action_row = create_actionrow(*buttons)
                    actions.append(action_row)
                    buttons = []
            if len(buttons):
                action_row = create_actionrow(*buttons)
                actions.append(action_row)

            res = await ctx.send(
                "img select",
                components=actions,
            )
            interaction = await wait_for_component(
                bot, components=actions,
            )
            await res.delete()
            await Image.get_pic(
                self, ctx, self.img_link[interaction.component_id]['url'],
                self.img_link[interaction.component_id]['name']
            )

    @img.command(description='melt picture')
    async def melt(self, ctx):
        """melt picture"""
        await Image.get_pic(
            self, ctx, self.img_link['melt']['url'],
            self.img_link['melt']['name'])

    @img.command(description='abya picture')
    async def abya(self, ctx):
        """abya picture"""
        await Image.get_pic(
            self, ctx, self.img_link['abya']['url'],
            self.img_link['abya']['name'])

    @img.command(description='shiran kedo~ picture')
    async def shiran(self, ctx):
        """shiran kedo~ picture"""
        await Image.get_pic(
            self, ctx, self.img_link['shiran']['url'],
            self.img_link['shiran']['name'])

    @img.command(description='party parrot GIF')
    async def party(self, ctx):
        """party parrot GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['party']['url'],
            self.img_link['party']['name'])

    @img.command(description='B picture')
    async def b_pic(self, ctx):
        """B picture"""
        await Image.get_pic(
            self, ctx, self.img_link['b_pic']['url'],
            self.img_link['b_pic']['name'])

    @img.command(description='gaming presentation GIF')
    async def presen(self, ctx):
        """gaming presentation GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['b_pic']['url'],
            self.img_link['b_pic']['name'])

    @img.command(description='maji yabakune')
    async def majiyaba(self, ctx):
        """maji yabakune"""
        await Image.get_pic(
            self, ctx, self.img_link['majiyaba']['url'],
            self.img_link['majiyaba']['name'])

    @img.command(description='bohe')
    async def bohe(self, ctx):
        """bohe"""
        await Image.get_pic(
            self, ctx, self.img_link['bohe']['url'],
            self.img_link['bohe']['name'])

    @img.command(description='gyu')
    async def gyu(self, ctx):
        """gyu GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['gyu']['url'],
            self.img_link['gyu']['name'])

    @img.command(description='ha!')
    async def ha(self, ctx):
        """ha! GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['ha']['url'],
            self.img_link['ha']['name'])

    @img.command(description='hello')
    async def hello(self, ctx):
        """hello GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['hello']['url'],
            self.img_link['hello']['name'])

    @img.command(description='maken')
    async def maken(self, ctx):
        """maken GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['maken']['url'],
            self.img_link['maken']['name'])

    @img.command(description='onegai')
    async def onegai(self, ctx):
        """onegai GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['onegai']['url'],
            self.img_link['onegai']['name'])

    @img.command(description='Pet the B')
    async def b_pet(self, ctx):
        """Pet the B GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['b_pet']['url'],
            self.img_link['b_pet']['name'])

    @img.command(description='thx')
    async def thx(self, ctx):
        """thx GIF"""
        await Image.get_pic(
            self, ctx, self.img_link['thx']['url'],
            self.img_link['thx']['name'])

    @commands.command(description='send photo')
    async def b_img(self, ctx, url: str, file_name: str):
        """b_img url file_name"""
        await Image.get_pic(self, ctx, url, file_name)

    async def get_pic(self, ctx, url: str, file_name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await Basic.send(self, ctx, 'server error... b')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, file_name))


#---------------------------------------------------------- AI系
class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='a3rt AI TalkAPI')
    async def ai(self, ctx, talk: str):
        """a3rt AI TalkAPI"""
        try:
            data = urllib.parse.urlencode({"apikey":_A3RT_KEY, "query":talk}).encode('utf-8')
            request = urllib.request.Request(_A3RT_URI, data)
            res = urllib.request.urlopen(request)
            json_load = json.load(res)
            # await Basic.send(self, ctx, '精度:'+str(json_load['results'][0]['perplexity'])+"\n"+json_load['results'][0]['reply'])
            await Basic.send(self, ctx, json_load['results'][0]['reply'])
        except Exception as e:
            print(e)
            await bot.get_channel(LOG_C).send(str(e))

#---------------------------------------------------------- youtube-dl
class Youtube(commands.Cog):
    ytdl_opts = {
        'format' : 'bestaudio/best',
        # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'outtmpl': 'tmp/%(title)s.%(id)s.%(ext)s',
        'restrictfilenames': True,
        # 'noplaylist': True, # allow playlist
        'nocheckcertificate': True,
        # 'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        # 'source_address': '0.0.0.0'
    }
    # ytdl = youtube_dl.YoutubeDL(ytdl_opts)
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='youtube-dl audio only')
    async def ydl(self, ctx, url: str):
        """youtube-dl audio only [ org / max 8MB ]"""
        if 'soundcloud' in urllib.parse.urlparse(url).netloc: # soundcloud
            await self.ydl_m4a(ctx, url)
        else: # youtube (or niconico)
            filename = await self.ydl_proc(ctx, url, self.ytdl_opts)
            for i in range(len(filename)):
                await self.ydl_send(ctx, filename[i]['filename'])

    @commands.command(description='youtube-dl audio mp3')
    async def ydl_mp3(self, ctx, url: str):
        """youtube-dl audio only [ mp3 / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        filename = await self.ydl_proc(ctx, url, dict(self.ytdl_opts, **setOpt))
        for i in range(len(filename)):
            await self.ydl_send(ctx, filename[i]['filename'])

    @commands.command(description='youtube-dl audio m4a')
    async def ydl_m4a(self, ctx, url: str):
        """youtube-dl audio only [ m4a / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }
        filename = await self.ydl_proc(ctx, url, dict(self.ytdl_opts, **setOpt))
        for i in range(len(filename)):
            await self.ydl_send(ctx, filename[i]['filename'])
        # await Basic.send(self, ctx, json.dumps(self.ytdl_opts | setOpt)) #Debug

    @commands.command(description='youtube-dl audio aac')
    async def ydl_aac(self, ctx, url: str):
        """youtube-dl audio only [ aac / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
            }]
        }
        filename = await self.ydl_proc(ctx, url, dict(self.ytdl_opts, **setOpt))
        for i in range(len(filename)):
            await self.ydl_send(ctx, filename[i]['filename'])
        # await Basic.send(self, ctx, json.dumps(self.ytdl_opts | setOpt)) #Debug

    async def ydl_getc(self, ctx, url:str, ytdl_opts):
        """" get playlist """
        async with ctx.typing():
            try:
                with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                    pre_info = ydl.extract_info(url, download=False)
                if 'entries' in pre_info:
                    video = pre_info['entries']
                    plist = []
                    for i, item in enumerate(video):
                        plist.append({'title':pre_info['entries'][i]['title'],'url':pre_info['entries'][i]['webpage_url']})
                    return plist
                else:
                    return [{'title':pre_info['title'],'url':url}]
            except Exception as e:
                print(e)
                await bot.get_channel(LOG_C).send(str(e))
                return False

    async def ydl_proc(self, ctx, url:str, ytdl_opts):
        """" download video & return title + filename """
        async with ctx.typing():
            try:
                # 事前に情報取得
                with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                    pre_info = ydl.extract_info(url, download=False)
                if 'entries' in pre_info:
                    # playlist (multiple video)
                    video = pre_info['entries']
                    res = []
                    for i, item in enumerate(video):
                        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                            info = ydl.extract_info(pre_info['entries'][i]['webpage_url'], download=True)
                            filename = ydl.prepare_filename(info)
                            title = info['title']
                            if 'postprocessors' in ytdl_opts:
                                filename = str(pathlib.Path(filename).with_suffix('.'+ytdl_opts['postprocessors'][0]['preferredcodec']))
                            res.append({'title':title, 'filename':filename})
                    return res
                else:
                    # single video
                    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                        info = pre_info
                        # info = ydl.extract_info(url, download=True)
                        title = info['title']
                        filename = ydl.prepare_filename(info)

                        dl_thread = threading.Thread(target = ydl.extract_info, args=(url,))
                        dl_thread.setDaemon(True)
                        dl_thread.start()
                        dl_thread.join()

                        if 'postprocessors' in ytdl_opts:
                            filename = str(pathlib.Path(filename).with_suffix('.'+ytdl_opts['postprocessors'][0]['preferredcodec']))
                        return [{'title':title, 'filename':filename}]
            except Exception as e:
                await Basic.send(self, ctx, 'Error: Youtube.ydl_proc')
                await bot.get_channel(LOG_C).send(str(e))
                return False

    def ydl_pre(self, url:str, ytdl_opts):
        """ pre yt download """
        try:
            with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return
        except Exception as e:
            print(e)
            return

    # convert (need install ffmpeg) fmt = m4a, mp3, ...
    async def ffmpeg(self, filename:str, fmt):
        stream = ffmpeg.input(filename)
        stream = ffmpeg.output(stream, filename+'.'+fmt, format=fmt)
        ffmpeg.run(stream)
        try:
            os.remove(filename)
        finally:
            return filename+'.'+fmt

    async def ydl_send(self, ctx, filename):
        try:
            with open(filename, 'rb') as fp:
                await ctx.send(file=discord.File(fp, filename))
                if os.path.exists(filename):
                    os.remove(filename)
        except discord.errors.HTTPException:
            await Basic.send(self, ctx, 'Error: File size is too large? [Max 8MB]\n')
        except Exception as e:
            print(e)
            # await Basic.send(self, ctx, 'Error: Unknown')
            await bot.get_channel(LOG_C).send(str(e))


#---------------------------------------------------------- Discord_VoiceChat
class VoiceChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now = None # now playing
        self.volume = 1.0 # music volume
        # self.voice_volume = 1.0 # voice volume
        self.inf_play = False # infinity play music
        self.queue = [] # music queue [{'title':'current music title', 'url':'current music url'},...]
        self.state = False # continue to play
        self.nightcore = False # nightcore effect
        self.bassboost = False # bassboost effect
        self.b_brand = False # b/b_loop selected brand name
        self.ytdl_opts = {
            'format' : 'bestaudio/best',
            # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'outtmpl': 'tmp/%(title)s.%(id)s.%(ext)s',
            'restrictfilenames': True,
            # 'noplaylist': True,
            'nocheckcertificate': True,
            # 'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            # 'source_address': '0.0.0.0'
        }
        self.ytdl_opts_np = {
            'format' : 'bestaudio/best',
            'outtmpl': 'tmp/%(title)s.%(id)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            # 'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            # 'source_address': '0.0.0.0'
        }
    @commands.command(description='Discord_VoiceChat Connect')
    async def v_connect(self, ctx):
        """Voice Connect"""
        if (not ctx.author.voice) or (not ctx.author.voice.channel): # ボイスチャンネルに入っていない
            await Basic.send(self, ctx, 'You need to be in the voice channel first.')
            return
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if not ctx.voice_client: # ボイスチャンネルに接続されていない場合
            await channel.connect(reconnect = True)

    @commands.command(description='Discord_VoiceChat Disconnect')
    async def v_disconnect(self, ctx):
        """Voice Disconnect"""
        self.inf_play = False
        self.queue = []
        self.state = False
        self.b_brand = False
        await ctx.voice_client.disconnect()

    @commands.command(description='same as v_disconnect')
    async def v_d(self, ctx):
        """Voice Disconnect (same as ?v_disconnect)"""
        await VoiceChat.v_disconnect(self, ctx)

    @commands.command(description='Discord_VoiceChat TTS')
    async def v_boice(self, ctx, *tx:str):
        """Voice TTS (Japanese)"""
        await VoiceChat.make_tts(self, ctx, tx, 'ja', 1)

    @commands.command(description='same as v_boice')
    async def v_voice(self, ctx, *tx:str):
        """Voice TTS (Japanese) (same as ?v_boice)"""
        tx = ' '.join(tx)
        await VoiceChat.v_boice(self, ctx, tx)

    @commands.command(description='Discord_VoiceChat TTS EN')
    async def v_boice_en(self, ctx, *tx:str):
        """Voice TTS EN (English)"""
        await VoiceChat.make_tts(self, ctx, tx, 'en', 0)

    @commands.command(description='same as v_boice_en')
    async def v_voice_en(self, ctx, *tx:str):
        """Voice TTS EN (English) (same as v_boice_en)"""
        tx = ' '.join(tx)
        await VoiceChat.v_boice_en(self, ctx, tx)

    @commands.group(description='play music (b/b_loop/stop/skip/queue/play)')
    async def v_music(self, ctx):
        """play music. (b/b_loop/b_list/stop/skip/queue/queue_del/play)"""
        await VoiceChat.v_connect(self, ctx) # 接続確認

        if ctx.invoked_subcommand is None: # サブコマンドがない場合
            self.state = False # auto play: off
            self.inf_play = False # stop inf play
            tx = str(ctx.message.content).split()[1] # サブコマンドではない場合、URLとして扱う
            if not tx or len(tx) <= 0:
                await Basic.send(self, ctx, 'The URL value is not appropriate')
                return
            try: # try connect url
                f = urllib.request.urlopen(tx)
                f.close()
            except Exception as e:
                print(e)
                await Basic.send(self, ctx, 'network error')
                await bot.get_channel(LOG_C).send(str(e))
                return False
            if self.now != None and self.state != True:
                self.now.stop()
                self.now = None

            await ctx.message.delete()
            pre_send = await Basic.send(self, ctx, "Starting the process...")
            plist = await Youtube.ydl_getc(self, ctx, tx, self.ytdl_opts)
            if plist:
                self.queue.extend(plist)
            if self.now == None and len(self.queue):
                if len(self.queue) > 1: # 複数曲の場合 (曲の表示等あり)
                    await Basic.edit(self, pre_send, str(len(plist))+" songs added ("+str(len(self.queue))+" songs in the queue)")
                else: await Basic.delete(self, pre_send)
                await VoiceChat.play(self, ctx)
            else:
                await Basic.edit(self, pre_send, 'ydl_getc error')
                return False

    @v_music.command(description='skip')
    async def skip(self, ctx):
        """skip current music"""
        # self.inf_play = False # infiniry play: off
        self.now.stop()
        self.now = None
        # if self.now != None:
        #     self.now.stop()
        #     self.now = None
        # if self.inf_play:
        #     self.now.stop()
        #     self.now = None
        #     pass # b_loopの時は、self.nowを停止してself.now = Noneにすると自動的に次の曲になるので.
        # elif len(self.queue) > 0:
        #     self.queue.pop(0)
        #     if len(self.queue) > 0:
        #         await VoiceChat.play(self, ctx)

    @v_music.command(description='stop')
    async def stop(self, ctx):
        """stop music"""
        self.state = False # auto play: off
        if self.now != None:
            self.now.stop()
            self.now = None
            self.inf_play = False
            self.state = False

    @v_music.command(description='pause music')
    async def pause(self, ctx):
        """pause music"""
        if self.now != None and not self.now.is_paused():
            self.now.pause()
        else:
            await Basic.send(self, ctx, 'No song is currently playing')

    @v_music.command(description='resume music')
    async def resume(self, ctx):
        """resume paused music"""
        if self.now != None and self.now.is_paused():
            self.now.resume()
        else:
            await Basic.send(self, ctx, 'The song has not been paused')

    @v_music.command(description='random play!')
    async def b(self, ctx):
        """One song from Mr. B's recommendation"""
        self.state = False # auto play: off
        self.inf_play = False # stop inf play
        if self.now != None:
            self.now.stop()
            self.now = None
        pre_send = await Basic.send(self, ctx, "Now processing...")

        sp_tmp = str(ctx.message.content).split()
        if len(sp_tmp) >= 3: # 再生するブランド名が指定された場合
            self.b_brand = ' '.join(sp_tmp[2:])
            brand_n, mm = my_music.get_brand_music(self.b_brand)
        else:
            self.b_brand = False
            brand_n, mm = my_music.get_music() # 1曲ランダムに取り出し

        filename_ = await Youtube.ydl_proc(self, ctx, mm['url'], self.ytdl_opts_np)
        if filename_:
            # print(filename_)
            filename = filename_[0]['filename']
            filename = await VoiceChat.effect(self, filename) # エフェクト
            # await Basic.send(self, ctx, f'`{brand_n}` - `{mm["title"]}`')
            await Basic.delete(self, pre_send)
            await Basic.send(self, ctx, f'```ini\n[TITLE] {brand_n} - {mm["title"]}\n[ URL ] {mm["url"]}```')
            await VoiceChat.voice_send(self, ctx, filename)

    @v_music.command(description='infinity random play!')
    async def b_loop(self, ctx):
        """infinity random play!
           select brand -> ?v_music b_loop "brand name"
        """
        self.state = False # auto play: off
        if self.now != None:
            self.now.stop()
            self.now = None
        self.inf_play = True # infiniry play: on

        sp_tmp = str(ctx.message.content).split()
        if len(sp_tmp) >= 3: # 再生するブランド名が指定された場合
            self.b_brand = ' '.join(sp_tmp[2:])
        else:
            self.b_brand = False

        while self.inf_play:
            if self.b_brand: # 再生するブランド名が指定されている場合
                brand_n, mm = my_music.get_brand_music(self.b_brand)
            else:
                brand_n, mm = my_music.get_music() # 1曲ランダムに取り出し

            pre_send = await Basic.send(self, ctx, "Now processing...")
            filename_ = await Youtube.ydl_proc(self, ctx, mm['url'], self.ytdl_opts_np)
            if not filename_ and self.now == None: # youtube_dl error
                # await Basic.send(self, ctx, 'Error: Youtube.ydl_proc')
                await Basic.delete(self, pre_send)
                print('Error: Youtube.ydl_proc')
                continue
            elif self.now == None: # 正常
                # try:
                filename = filename_[0]['filename']
                filename = await VoiceChat.effect(self, filename) # エフェクト
                # await Basic.send(self, ctx, f'`{brand_n}` - `{mm["title"]}`')
                await Basic.delete(self, pre_send)
                await Basic.send(self, ctx, f'```ini\n[TITLE] {brand_n} - {mm["title"]}\n[ URL ] {mm["url"]}```')
                await VoiceChat.voice_send(self, ctx, filename)
                # except:
                #     await Basic.send(self, ctx, 'Error: Youtube.voice_send')
            else:
                await Basic.delete(self, pre_send)
                break

    @v_music.command(description='b/b_loop brand list')
    async def b_list(self, ctx):
        """b/b_loop brand list"""
        brand_list = my_music.get_brand_list()
        await Basic.send(self, ctx, '```c\n// b/b_loopで再生されるADVのブランド一覧\n'+', '.join(brand_list)+'```')

    @v_music.command(description='play')
    async def play(self, ctx):
        """play queue"""
        self.state = True
        try:
            if self.now.is_paused(): # 既にpauseされていた場合
                self.now.resume()
        except: pass
        if len(self.queue) <= 0:
            await Basic.send(self, ctx, 'queue = Null')
        while len(self.queue):
            if self.now == None:
                try:
                    pre_send = await Basic.send(self, ctx, "Now processing...")
                    next_song = self.queue.pop(0)
                    next_song_filename = await Youtube.ydl_proc(self, ctx, next_song['url'], self.ytdl_opts)
                    next_song_title = next_song_filename[0]['title']
                    next_song_filename = await VoiceChat.effect(self, next_song_filename[0]['filename']) # エフェクト

                    # if len(self.queue) > 0: # 別スレッドで次の曲を事前にダウンロードする
                    #     next_q = self.queue[0]['url']
                    #     next_th = threading.Thread(target = Youtube.ydl_pre, args=(self, next_q, self.ytdl_opts,))
                    #     next_th.start()

                    await Basic.edit(self, pre_send, f'```ini\n[TITLE] {next_song_title}\n[ URL ] {next_song["url"]}```')
                    await VoiceChat.voice_send(self, ctx, next_song_filename)
                except Exception as e:
                    print(e)
                    await bot.get_channel(LOG_C).send(str(e))
                    # await Basic.send(self, ctx, "Error: VoiceChat.play")

                    continue
            if len(self.queue) <= 0 or not self.state:
                break

    @v_music.command(description='show queue')
    async def queue(self, ctx):
        """show queue"""
        if len(self.queue) > 0:
            sd = f'> | {self.queue[0]["title"]}\n'
            for i in range(1, len(self.queue)):
                sd += f'{i} | {self.queue[i]["title"]}\n'
            await Basic.send(self, ctx, "```py\n"+sd+"```")
        else:
            await Basic.send(self, ctx, "queue = Null")

    @v_music.command(description='delete queue')
    async def del_queue(self, ctx):
        """delete queue"""
        self.queue = []
        await Basic.send(self, ctx, "deleted queue")

    @v_music.command(description='nightcore effect toggle')
    async def nightcore(self, ctx):
        self.nightcore = True if not self.nightcore else False
        await Basic.send(self, ctx, "nightcore = "+str(self.nightcore))

    @v_music.command(description='bassboost effect toggle')
    async def bassboost(self, ctx):
        self.bassboost = True if not self.bassboost else False
        await Basic.send(self, ctx, "bassboost = "+str(self.bassboost))

    # @v_music.command(description='loop the currently playing music')

    # @commands.command(description='play music + kawaii_voice_gtts.music_pack1')
    # async def v_music_pack1(self, ctx, tx:str):
    #     """play music + kawaii_voice_gtts.music_pack1"""
    #     try: # try connect url
    #         f = urllib.request.urlopen(tx)
    #         f.close()
    #     except: return False

    #     ytdl_opts = {
    #         'format' : 'bestaudio/best',
            # # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            # 'outtmpl': '%(title)s%(id)s.%(ext)s',
    #         'restrictfilenames': True,
    #         'noplaylist': True, # not allow playlist
    #         'nocheckcertificate': True,
    #         'no_warnings': True,
    #         'default_search': 'auto',
    #         'source_address': '0.0.0.0',
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #         }]
    #     }
    #     if tx.lower() == 'stop' and self.now != None:
    #         self.now.stop()
    #         self.now = None
    #     filename_ = await Youtube.ydl_proc(self, ctx, tx, ytdl_opts)
    #     if not filename_ and self.now == None:
    #         await Basic.send(self, ctx, 'Error; Youtube.ydl_proc')
    #         return False
    #     elif self.now == None: # 正常
    #         try:
    #             filename = filename_[0]
    #             imouto = kawaii_voice_gtts.kawaii_voice(filename)
    #             imouto = imouto.music_pack1()
    #             imouto.audio.export(filename, 'mp3')
    #             await VoiceChat.voice_send(self, ctx, filename)
    #         except:
    #             await Basic.send(self, ctx, 'Error: kawaii_voice_gttx.kawaii_voice, imouto.music_pack1, Youtube.voice_send')

    async def make_tts(self, ctx, text, lg, k_option): # text=text, lg=language, k_option=kawaii_voice_gtts(0=false, 1=true)
        text = ' '.join(text)
        pool = string.ascii_letters + string.digits
        randm = ''.join(random.choice(pool) for _ in range(16))
        filename = str(randm) + ".mp3"
        gTTS(str(text), lang=lg).save(filename)

        if k_option == 1:
            imouto = kawaii_voice_gtts.kawaii_voice(filename)
            imouto = imouto.pitch(0.4)
            imouto.audio.export(filename, 'mp3')

        if not hasattr(ctx.message, 'guild') or not hasattr(ctx.message.guild, 'voice_client'): # join voice channel
            try:
                await ctx.author.voice.channel.connect(reconnect = True)
            except Exception as e:
                print(e)
                await bot.get_channel(LOG_C).send(str(e))
        await VoiceChat.voice_send(self, ctx, filename)

    async def effect(self, filename):
        if self.nightcore == False and self.bassboost == False: # オプションがない場合
            return filename
        org_filename = filename
        split_filename = os.path.basename(filename).split('.')
        split_filename_ext = split_filename.pop(len(split_filename)-1) # ファイルの拡張子を除く
        if split_filename_ext != 'mp3':
            try:
                tmp_audio = ffmpeg.input(filename)
                tmp_audio_enc = ffmpeg.output(tmp_audio, str('.'.join(split_filename))+'.mp3', format='mp3')
                ffmpeg.run(tmp_audio_enc)
                try: os.remove(org_filename) # ファイル形式の変換前のファイルを削除
                except Exception as e: print(e)
                filename = str('.'.join(split_filename))+'.mp3'
            except Exception as e:
                print(e)
                await bot.get_channel(LOG_C).send(str(e))
                # await Basic.send('Error: VoiceChat.effect')
                return filename
        imouto = kawaii_voice_gtts.kawaii_voice(filename)
        if self.nightcore:
            imouto = imouto.music_pack1()
        if self.bassboost:
            imouto = imouto.bass_boost(0)
        imouto.audio.export(filename, 'mp3') # 保存
        return filename

    async def voice_send(self, ctx, filename):
        if hasattr(self, 'now') and self.now != None:
            self.now.stop()
        if os.path.exists(filename): # ファイル存在確認
            if hasattr(self, 'volume') and self.volume == 1.0: audio_source = discord.FFmpegPCMAudio(filename)
            else:
                self.volume = 1.0
                audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), volume=self.volume)

            if not hasattr(ctx, 'voice_client'): # ボイスチャンネルに接続されていない場合
                await ctx.author.voice.channel.connect(reconnect = True)
            self.now = ctx.voice_client
            try:
                self.now.play(audio_source) # 再生
                while ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused():
                    await asyncio.sleep(1)
            except Exception as e:
                print(e)
                self.inf_play = False
                self.state = False
                await bot.get_channel(LOG_C).send(str(e))
                # await VoiceChat.v_connect(self, ctx)

            os.remove(filename)
            self.now = None

    @commands.command(description='change music volume')
    async def v_volume(self, ctx, vol:str):
        """change music volume"""
        try:
            if float(vol) > 1.0: vol = 1.0
            elif float(vol) < 0: vol = 0.0 
            self.volume = float(vol)
        except:
            self.volume = 1.0
        await Basic.send(self, ctx, 'volume : '+str(self.volume))

    @commands.command(description='Channel member list')
    async def v_list(self, ctx):
        """channel member list"""
        channel = ctx.author.voice.channel
        out = ''
        cnt = 1
        for ch in channel.guild.voice_channels:
            if len(ch.members)>0 and len(out)>0: # メンバーがいて、2番目以降
                out += '-\n'
            for member in ch.members:
                out += str(cnt) +' | '+ str(member) + '\n'
                cnt += 1
            #     await member.move_to(None)
        await Basic.send(self, ctx, '```py\n'+out+'```')

    @commands.command(description='voice mute')
    async def v_mute(self, ctx, no):
        """voice mute. (b = all)"""
        channel = ctx.author.voice.channel
        if str(no).lower() == 'b': # 全員
            for ch in channel.guild.voice_channels:
                for member in ch.members:
                    await member.edit(mute = True)
        else: # 通常のミュート
            try:
                no = int(no)
                if no <= 0: return
            except: return
            cnt = 0
            for ch in channel.guild.voice_channels:
                for member in ch.members:
                    cnt += 1
                    if str(cnt) == str(no):
                        await member.edit(mute = True)

    @commands.command(description='voice unmute')
    async def v_unmute(self, ctx, no):
        """voice unmute. (b = all)"""
        channel = ctx.author.voice.channel
        if str(no).lower() == 'b': # 全員
            for ch in channel.guild.voice_channels:
                for member in ch.members:
                    await member.edit(mute = False)
        else: # 通常のアンミュート
            try:
                if int(no) <= 0: return
            except: return
            cnt = 0
            for ch in channel.guild.voice_channels:
                for member in ch.members:
                    cnt += 1
                    if str(cnt) == str(no):
                        await member.edit(mute = False)

    @commands.command(description='Discord_VoiceChat ALL D')
    async def v_bd(self, ctx):
        """Voice ALL D"""
        channel = ctx.author.voice.channel
        for ch in channel.guild.voice_channels:
            for member in ch.members:
                await member.move_to(None)

    @commands.command(description='add queue')
    async def v_add(self, ctx, tx):
        """add queue"""
        if not tx:
            await Basic.send('The URL value is not appropriate')
            return False
        try: # try connect music url
            f = urllib.request.urlopen(tx)
            f.close()
        except Exception as e:
            print(e)
            await Basic.send(self, ctx, 'Network error')
            await bot.get_channel(LOG_C).send(str(e))
            return False
        pre_send = await Basic.send(self, ctx, "Now processing...")
        plist = await Youtube.ydl_getc(self, ctx, tx, self.ytdl_opts)
        self.queue.extend(plist)
        await Basic.delete(self, pre_send)
        await Basic.send(self, ctx, str(len(plist))+" songs added ("+str(len(self.queue))+" songs in the queue)")

#---------------------------------------------------------- ASCII Encode
class Encode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='ASCII Encode')
    async def asc_enc(self, ctx, *text:str):
        """ASCII Encode"""
        text = ' '.join(text)
        send = ''
        for i in range(len(text)):
            send += ' ' + str(ord(text[i]))
        await Basic.send(self, ctx, send)

    @commands.command(description='ASCII Decode')
    async def asc_dec(self, ctx, *text:int):
        """ASCII Decode"""
        send = ''
        for i in range(len(text)):
            send += chr(text[i])
        await Basic.send(self, ctx, send)

#---------------------------------------------------------- GoogleTranslate
class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Translate en -> ja')
    async def trans(self, ctx, *text):
        """Translate  English -> Japanese"""
        gReq = '?text='+str(' '.join(text))+'&source=en&target=ja'
        await Translate.transA(self, ctx, _GoogleTranslateAPP_URL+gReq)

    @commands.command(description='Translate ja -> en')
    async def transJ(self, ctx, *text):
        """Translate Japanese -> English"""
        gReq = '?text='+str(' '.join(text))+'&source=ja&target=en'
        await Translate.transA(self, ctx, _GoogleTranslateAPP_URL+gReq)

    async def transA(self, ctx, uri:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as res:
                if res.status == 200:
                    res_json = await res.json()
                    await Basic.send(self, ctx, res_json['res'])

#---------------------------------------------------------- Timer
class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Timer (s)')
    async def timer(self, ctx, time_set:float):
        """Timer (s)"""
        mention = str(ctx.message.author.mention)
        dest = await Basic.send(self, ctx, "Ready!")
        start = time.time()
        while float(time_set)-float(time.time()-start) > 0:
            left = str('{:.1f}'.format(float(time_set)-float(time.time()-start)))
            await dest.edit(content = f'{mention}'+" | left: "+left+'s')
            await asyncio.sleep(1)
        await dest.edit(content = f'{mention}'+" | Time up!")

    @commands.command(description='pomodoro set, work(min), break(min)')
    async def pomodoro(self, ctx, *tset:float):
        """
        pomodoro set, work(min), break(min)
        default 25min+5min x 4set
        """
        if len(tset)>=1 : setCnt_ = tset[0]
        else: setCnt_ = 4 # 4set
        if len(tset)>=2 : time_ = tset[1] * 60
        else: time_ = 1500 # 25min
        if len(tset)>=3 : time2_ = tset[2] * 60
        else: time2_ = 300 # 5min

        dest = await Basic.send(self, ctx, "Ready!")
        mention = str(ctx.message.author.mention)
        setCnt = setCnt_
        while setCnt > 0:
            times, time2 = time_, time2_ # reset time
            start = time.time()
            while float(times)-float(time.time()-start) > 0: # work
                left = int(float(times)-float(time.time()-start))
                await dest.edit(content = f'{mention}'+" | "+str(setCnt_ - setCnt + 1)+"/"+str(setCnt_)+" work left: "+ str(int(left/60)).zfill(2)+":"+str(int(left%60)).zfill(2))
                await asyncio.sleep(1)
            while float(time2)-float(time.time()-start) > 0: # break
                left = int(float(time2)-float(time.time()-start))
                await dest.edit(content = f'{mention}'+" | "+str(setCnt_ - setCnt + 1)+"/"+str(setCnt_)+" break left: "+ str(int(left/60)).zfill(2)+":"+str(int(left%60)).zfill(2))
                await asyncio.sleep(1)
            setCnt -= 1
        await dest.edit(content = f'{mention}'+" Good jobbb!\nRecord: cnt="+str(setCnt_)+", work: "+str(int(time_/60))+"(min) / break: "+str(int(time2_/60))+"(min)")

#---------------------------------------------------------- BrainF*ck
class BrainFuck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Exec BrainF*ck')
    async def bf(self, ctx, *tx:str):
        """Exec BrainF*ck"""
        tx = ''.join(tx)
        bfc = brainfuck.BrainFuck(tx, 0).bf()
        await Basic.send(self, ctx, bfc.out_asc)

    @commands.command(description='Debug BrainF*ck')
    async def bf_debug(self, ctx, *tx:str):
        """Debug BrainF*ck"""
        tx = ''.join(tx)
        bfc = brainfuck.BrainFuck(tx, 4).bf()
        # if len(bfc.debug) > 2000:
        await Basic.send(self, ctx, bfc.debug)

#---------------------------------------------------------- URL
class URL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Generate Shorter URL')
    async def url_short(self, ctx, tx:str):
        """Generate shorter url"""
        await Basic.send(self, ctx, Shortener().tinyurl.short(tx))

    @commands.command(description='Restore the shortened URL')
    async def url_expand(self, ctx, tx:str):
        """Restore the shortened URL"""
        await Basic.send(self, ctx, Shortener().tinyurl.expand(tx))

    @commands.command(description='URL encode')
    async def url_enc(self, ctx, *tx:str):
        """URL encode"""
        s = ' '.join(tx)
        await Basic.send(self, ctx, urllib.parse.quote(s))

    @commands.command(description='URL decode')
    async def url_dec(self, ctx, *tx:str):
        """URL decode"""
        s = ' '.join(tx)
        await Basic.send(self, ctx, urllib.parse.unquote(s))

#---------------------------------------------------------- Slash
class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def logger(self, ctx):
        lChannel = self.bot.get_channel(LOG_C)
        await lChannel.send("```"\
            +"\nGuild  : "+str(ctx.guild_id)
            +"\nChannel: "+str(ctx.channel_id)\
            +"\nAuthor : "+str(ctx.author.name)+"#"\
            +str(ctx.author.discriminator)+" (ID: "+str(ctx.author.id)+")"\
            +"\n/"+str(ctx.command)+" "+str(' '.join(ctx.args))+"```")

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx:SlashContext):
        """ping test"""
        await Basic.send(self, ctx, f"{bot.latency*1000}ms")
        await self.logger(ctx)

    @cog_ext.cog_slash(name="hattori")
    async def hattori(self, ctx:SlashContext):
        """hello, htr!"""
        await B.hattori(self, ctx)
        await self.logger(ctx)

    @cog_ext.cog_slash(name="ydl")
    async def ydl(self, ctx:SlashContext, url:str):
        await Youtube.ydl(self, ctx, url)
        await self.logger(ctx)

    @cog_ext.cog_slash(name="ydl_m4a")
    async def ydl_m4a(self, ctx:SlashContext, url:str):
        await Youtube.ydl_m4a(self, ctx, url)
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_connect")
    async def v_connect(self, ctx:SlashContext):
        """connect to voice chat"""
        await VoiceChat.v_connect(self, ctx)
        await Basic.send_hidden(self, ctx, 'connected')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_disconnect")
    async def v_disconnect(self, ctx:SlashContext):
        """disconnect from voice chat"""
        await VoiceChat.v_disconnect(self, ctx)
        await Basic.send_hidden(self, ctx, 'disconnected')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_voice")
    async def v_voice(self, ctx:SlashContext, tx:str):
        await VoiceChat.v_boice(self, ctx, tx)
        await Basic.send_hidden(self, ctx, 'b')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_voice_en")
    async def v_voice_en(self, ctx:SlashContext, tx:str):
        await VoiceChat.v_boice_en(self, ctx, tx)
        await Basic.send_hidden(self, ctx, 'b')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_bd")
    async def v_bd(self, ctx:SlashContext):
        await VoiceChat.v_bd(self, ctx)
        await Basic.send_hidden(self, ctx, 'v_bd')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_music")
    async def v_music(self, ctx:SlashContext):
        # print(vars(ctx))
        vc_c = VoiceChat(self.bot)
        await VoiceChat.v_music(vc_c, ctx)
        await Basic.send_hidden(self, ctx, 'v_music')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="v_volume")
    async def v_volume(self, ctx:SlashContext, volume:str):
        await VoiceChat.v_volume(self, ctx, volume)
        await self.logger(ctx)

    @cog_ext.cog_slash(name="send")
    async def send(self, ctx:SlashContext, tx:str):
        ch = ctx.channel_id
        ch_s = bot.get_channel(ch)
        await ch_s.send(tx)
        await Basic.send_hidden(self, ctx, 'ok')
        await self.logger(ctx)

    @cog_ext.cog_slash(name="img")
    async def img(self, ctx:SlashContext):
        img_c = Image(self.bot)
        await Image.img(img_c, ctx)
        await Basic.send_hidden(self, ctx, 'ok')
        await self.logger(ctx)


#---------------------------------------------------------- Archive
class Archive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="message counter **CAUTION**")
    async def ms_cnt(self, ctx):
        """message counter (count this channel) / This will take a long time."""
        cnt = {}
        cc = 0
        await Basic.send(self, ctx, "This will take a long time.")
        pre_send = await Basic.send(self, ctx, "Now processing...")
        try:
            async for message in ctx.channel.history(limit = None):
                user_id = str(message.author.name) + '#' + str(message.author.discriminator)
                cc += 1
                if user_id not in cnt: cnt[user_id] = 1
                else:
                    cnt[user_id] += 1
                # if message.auther == ctx.message.author:
                #     cnt += 1
            await Basic.delete(self, pre_send)
            res = '```hs\nchannel name:' + str(urllib.parse.unquote(ctx.channel.name)) + ' / id:' + str(ctx.channel.id) + '\n'
            for key, val in cnt.items():
                url_dec = urllib.parse.unquote(key)
                res += str(url_dec) + ' -> ' + str(val) + '\n'
            res += '```'
        except Exception as e:
            print(e)
            await bot.get_channel(LOG_C).send(str(e))
            await Basic.delete(self, pre_send)
            await Basic.send(self, ctx, 'Error: Archive.ms_cnt / 429 Too Many Requests?')
            return False
        await Basic.send(self, ctx, res)

    @commands.group(description="Simple text archiving")
    async def archive(self, ctx):
        """Simple text archiving (only this channel)"""
        if ctx.invoked_subcommand is None:
            try:
                pre_send = await Basic.send(self, ctx, "only 100 will be archived\nNow processing...")
                buf = '```\nchannel name:' + str(urllib.parse.unquote(ctx.channel.name)) + ' / id:' + str(ctx.channel.id) + '\n'
                ms_cnt = 0
                async for message in ctx.channel.history():
                    ms_cnt += 1
                    user_id = str(urllib.parse.unquote(message.author.name)) + '#' + str(message.author.discriminator)
                    # https://discordpy.readthedocs.io/en/latest/api.html#discord.Message.attachments
                    # https://discordpy.readthedocs.io/en/latest/api.html#discord.Attachment.url
                    atc = ''
                    if message.attachments:
                        atc = ' '
                        for i in range(len(message.attachments)):
                            atc += ' '+message.attachments[i].url
                    buf = user_id + ' ' + str(message.created_at) + ' ' + str(message.content).replace('\n', '') + str(atc) + '\n' + buf
                buf += '```'
                await Basic.delete(self, pre_send)
            except Exception as e:
                print(e)
                await bot.get_channel(LOG_C).send(str(e))
                await Basic.delete(self, pre_send)
                await Basic.send(self, ctx, 'Error: Archive.ms_cnt / 429 Too Many Requests?')
                return False
            await Basic.send(self, ctx, buf)

    @archive.command(description='full archiving **CAUTION**')
    async def full(self, ctx):
        """Full archive of this channel. This will take a long time."""
        try:
            pre_send = await Basic.send(self, ctx, "This will take a long time.\nNow processing...")
            buf = '```\nchannel name:' + str(urllib.parse.unquote(ctx.channel.name)) + ' / id:' + str(ctx.channel.id) + '\n'
            ms_cnt = 0
            async for message in ctx.channel.history(limit = None):
                ms_cnt += 1
                user_id = str(urllib.parse.unquote(message.author.name)) + '#' + str(message.author.discriminator)
                atc = ''
                if message.attachments:
                    atc = ' '
                    for i in range(len(message.attachments)):
                        atc += ' '+message.attachments[i].url
                buf = user_id + ' ' + str(message.created_at) + ' ' + str(message.content).replace('\n', '') + str(atc) + '\n' + buf
            buf += '```'
            await Basic.delete(self, pre_send)
        except Exception as e:
            print(e)
            await bot.get_channel(LOG_C).send(str(e))
            await Basic.delete(self, pre_send)
            await Basic.send(self, ctx, 'Error: Archive.ms_cnt / 429 Too Many Requests?')
            return False
        await Basic.send(self, ctx, buf)

#---------------------------------------------------------- Basic
class Basic():
    def __init__(self, bot):
        self.bot = bot

    async def get_random(n):
        base = string.digits + string.ascii_lowercase + string.ascii_uppercase
        return str(''.join([random.choice(base) for _ in range(n)]))

    async def send(self, ctx, tx):
        """ 
        文字の送信

        サイズが大きい場合は、テキストファイルにして送信
        さらに大きい場合はzip圧縮して送信
        """
        dt_nt = datetime.datetime.now()
        send_fname = 'res_'+str(dt_nt.strftime('%Y%m%d%H%M%S'))
        if len(str(tx)) <= 2000: # 2000文字以下
            return await ctx.send(str(tx))
        elif sys.getsizeof(str(tx)) <= 8*1024**2-1: # 8MB未満
            try:
                data = io.StringIO(str(tx))
                return await ctx.send(file=discord.File(data, send_fname+'.txt'))
            except Exception as e: # サイズ上限?
                print(e)
                await ctx.send('Error: Basic.send (text file)')
                await bot.get_channel(LOG_C).send(str(e))
                return False
        else:
            try:
                dt_n = datetime.datetime.now()
                zname = str(dt_n.strftime('%Y%m%d%H%M%S%f')) + str(secrets.token_hex(16))
                with open(zname+'.txt', mode='w') as f:
                    f.write(str(tx))
                with zipfile.ZipFile(zname+'.zip', 'w', compression=zipfile.ZIP_DEFLATED) as n_z:
                    n_z.write(zname+'.txt', arcname=send_fname+'.txt')
                resp = await ctx.send(file=discord.File(zname+'.zip', send_fname+'.zip'))
                try:
                    os.remove(zname+'.txt')
                    os.remove(zname+'.zip')
                except Exception as e: print(e)
                return resp

            except Exception as e:
                print(e)
                await ctx.send('Error: Size limit has been exceeded?')
                await bot.get_channel(LOG_C).send(str(e))
                return False

    async def send_hidden(self, ctx, tx):
        """ コマンドを実行したクライアントにのみ送信 (Basic.sendのようにサイズの大きいテキストは送れない) """
        await ctx.send(content=tx, hidden=True)

    async def edit(self, res, tx):
        """ 送信した内容の編集 """
        dt_nt = datetime.datetime.now()
        send_fname = 'res_'+str(dt_nt.strftime('%Y%m%d%H%M%S'))
        if len(str(tx)) <= 2000 and len(str(tx)) > 0: # 2000字以下 1文字以上
            return await res.edit(content = str(tx))
        elif len(str(tx)) <= 0: # 0文字以下の時は削除
            await Basic.delete(self, res)
        elif sys.getsizeof(str(tx)) <= 8*1024**2-1: # 8MB未満
            try:
                data = io.StringIO(str(tx))
                return await res.edit(file=discord.File(data, send_fname+'.txt'))
            except Exception as e:
                print(e)
                await res.send('Error: Basic.send (text file)')
                await bot.get_channel(LOG_C).send(str(e))
                return False
        else:
            try:
                dt_n = datetime.datetime.now()
                zname = str(dt_n.strftime('%Y%m%d%H%M%S%f')) + str(secrets.token_hex(16))
                with open(zname+'.txt', mode='w') as f:
                    f.write(str(tx))
                with zipfile.ZipFile(zname+'.zip', 'w', compression=zipfile.ZIP_DEFLATED) as n_z:
                    n_z.write(zname+'.txt', arcname=send_fname+'.txt')
                resp = await res.send(file=discord.File(zname+'.zip', send_fname+'.zip'))
                try:
                    os.remove(zname+'.txt')
                    os.remove(zname+'.zip')
                except Exception as e: print(e)
                return resp
            except Exception as e:
                print(e)
                await res.send('Error: Size limit has been exceeded?')
                await bot.get_channel(LOG_C).send(str(e))
                return False

    async def delete(self, res):
        """ 送信した内容の削除 """
        await res.delete()

# Botの起動とDiscordサーバーへの接続
bot.add_cog(Calc(bot))
bot.add_cog(B(bot))
bot.add_cog(Image(bot))
bot.add_cog(AI(bot))
bot.add_cog(Youtube(bot))
bot.add_cog(VoiceChat(bot))
bot.add_cog(Encode(bot))
bot.add_cog(Translate(bot))
bot.add_cog(Timer(bot))
bot.add_cog(BrainFuck(bot))
bot.add_cog(URL(bot))
bot.add_cog(Slash(bot))
bot.add_cog(Archive(bot))
bot.run(_TOKEN)
