# make requirements.txt command -> (myenv)$ pip freeze > requirements.txt
# Video and audio are file-like objects.

# This Discord bot uses PyNaCl & FFmpeg in VoiceChat class.

# pip update
# powershell: pip3 install --upgrade ((pip3 freeze) -replace '==.+','')
# https://www.yukkuriikouze.com/2019/07/12/3105/


from __future__ import unicode_literals

# ---- my module ----
import my_key # get my api keys
import my_music
import brainfuck # my brainfuck interpreter
import htr # get hattori
import htr_end
import htr_dead
import kawaii_voice_gtts
# ----- basic module ----
import os
import io
import re
import math
import random
import string
import json
import random
import socket
import time
import platform
import threading
# ----- extend module -----
import aiohttp #画像転送系
from pyshorteners import Shortener
from gtts import gTTS
import asyncio
import pathlib
import psutil
import cpuid
import youtube_dl
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
import urllib.request
import urllib.parse
from niconico_dl_async import NicoNico
import ffmpeg
# import requests #req


VERSION='v2.5.14'

TOKEN, A3RT_URI, A3RT_KEY, GoogleTranslateAPP_URL,\
    LOG_C, MAIN_C, VOICE_C, HA, UP_SERVER,\
    M_CALL = my_key.get_keys()

HTR_LIST = htr.get_hattori()
HTRE_LIST = htr_end.end_hattori()
HTRD_LIST = htr_dead.dead_hattori()

P2PEQ_URI='https://api.p2pquake.net/v1/human-readable'
# P2PEQ_URI='http://localhost:1011/p2p_ex/'
P2PEQ_INT=5 # GET interval (s)
P2PEW_NMIN=40 # Notification minimum earthquake scale
P2PEW_NMIN_LOG=20 # Notification minimum earthquake scale (log)

UP_SERVER_INT = 5 # up interval (min)

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
    # await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="BBBot "+VERSION+'beta', emoji="🍝"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="BBBot "+VERSION+'beta', emoji="🍝"))
    lChannel = bot.get_channel(LOG_C)
    await lChannel.send('BBBot is Ready! ' + VERSION)

    # 非同期並行処理
    await asyncio.gather(
        EqCheck(bot).p2peq_check(),
        UpServer(bot).up_server()
    )

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    lChannel = bot.get_channel(LOG_C)
    if message.content.startswith('?'):
        await lChannel.send("```\n@"+str(message.author.name)+"\n"+str(message.author.id)+"\n"+str(message.content)+" ```")
        await bot.process_commands(message)

#---------------------------------------------------------- 定期実行系
class EqCheck:
    def __init__(self, bot):
        self.bot = bot

    async def p2peq_check(self):
        # req = urllib.request.Request(P2PEQ_URI)
        res_log = [] # Earthquake log
        mChannel = bot.get_channel(MAIN_C)
        lChannel = bot.get_channel(LOG_C)

        while True:
            # print('req')
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(P2PEQ_URI) as res:
                        if res.status == 200:
                            res_json = await res.json()
                            # res_json = json.loads(body.decode('utf-8'))
                            for i in range(len(res_json)):
                                # print(res_json[i]['code'])
                                if int(res_json[i]['code']) == 551: # Earthquake Code
                                    # await mChannel.send(json.dumps(res_json[i]))
                                    # print(len(res_log))
                                    if len(res_log) <= 0: # 初回の処理
                                        res_log  = res_json[i]
                                    elif res_log != res_json[i] \
                                    and str(res_json[i]['earthquake']['maxScale']) != 'null'\
                                    and int(res_json[i]['earthquake']['maxScale']) >= P2PEW_NMIN \
                                    and res_json[i]['earthquake']['domesticTsunami'] != "Checking" :
                                        res_log  = res_json[i]
                                        await mChannel.send(await EqCheck.castRes(self, res_json, i))
                                        await lChannel.send(await EqCheck.castRes(self,res_json, i))
                                        # await lChannel.send(res_json)
                                    elif res_log != res_json[i] \
                                    and str(res_json[i]['earthquake']['maxScale']) != 'null'\
                                    and int(res_json[i]['earthquake']['maxScale']) >= P2PEW_NMIN_LOG:
                                        await lChannel.send(await EqCheck.castRes(self,res_json, i))
                                        res_log  = res_json[i]
                                    break

            except urllib.error.URLError as err:
                print(err.reason)
            await asyncio.sleep(P2PEQ_INT)

    async def castScale(self, scale: int):
        print(scale)
        if scale <= 40 or scale == 70:
            return str(int(scale/10))
        elif scale%10 == 5:
            return str(int(scale/10)+1)+"弱"
        else:
            return str(int(scale/10))+"強"

    async def castTsunami(self, status: str):
        if status == 'None':
            return 'なし'
        elif status == 'Unknown':
            return '不明'
        elif status == 'Checking':
            return '調査中'
        elif status == 'NonEffective':
            return '若干の海面変動 (被害の心配なし)'
        elif status == 'Watch':
            return '津波注意報'
        elif status == 'Warning':
            return '津波警報 (種類不明)'
        else:
            return status

    async def castRes(self, res_json, i: int):
        return "```yaml\n"\
            + "Earthquake : " + str(res_json[i]['time']) + "\n"\
            + "Place      : " + str(res_json[i]['earthquake']['hypocenter']['name'])\
            + " (" + str(res_json[i]['earthquake']['hypocenter']['latitude']) + " "\
            + str(res_json[i]['earthquake']['hypocenter']['longitude']) + ")\n"\
            + "Depth      : " + str(res_json[i]['earthquake']['hypocenter']['depth']) + "\n"\
            + "MaxScale   : " + await EqCheck.castScale(self, res_json[i]['earthquake']['maxScale'])+"\n"\
            + "Magnitude  : " + str(res_json[i]['earthquake']['hypocenter']['magnitude'])+"\n"\
            + "Tsunami    : " + await EqCheck.castTsunami(self, res_json[i]['earthquake']['domesticTsunami'])+"\n"\
            + "```"

class UpServer:
    def __init__(self, bot):
        self.bot = bot

    async def up_server(self):
        # lChannel = bot.get_channel(LOG_C)
        while True:
            # await lChannel.send('up server')
            try:
                for i in UP_SERVER:
                    req = urllib.request.Request(i)
                    with urllib.request.urlopen(req):
                        pass
                    # with urllib.request.urlopen(req) as res:
                    #     pass
                    #     body = res.read()
            except urllib.error.URLError:
                pass
            # except urllib.error.URLError as err:
            #     print(err.reason)
            #     pass

            await asyncio.sleep(60*UP_SERVER_INT)


#---------------------------------------------------------- 計算系
class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='計算 Eval')
    # Evalなので攻撃しないでください。
    async def calc(self, ctx, *inc: str):
        """Calc number Eval"""
        inc = ''.join(inc)
        inc = re.sub(r"[\u3000 \t]", "", inc)
        await ctx.send(eval(inc))
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
    @commands.command(description='自己情報量I()')
    async def self_info(self, ctx, p: str):
        """Self-information I(p)"""
        p = float(eval(p))
        if p == 0.0:
            await ctx.send(0.0)
        else:
            await ctx.send(-p*math.log2(p))
    @commands.command(description='エントロピー関数計算H()')
    async def ent(self, ctx, p: str):
        """EntropyFunc H(p)"""
        p = float(eval(p))
        if p == 0.0:
            await ctx.send(0.0)
        else:
            await ctx.send(-p*math.log2(p)-(1-p)*math.log2(1-p))
    @commands.command(description='乱数(int) 1~x')
    async def rand(self, ctx, p: str):
        """Random(int) 1~x"""
        p = int(eval(p))
        if p>1:
            await ctx.send(random.randint(1, p))
        else:
            await ctx.send(random.randint(p, 1))
    @commands.command(description='乱数(float)) 1.0~x')
    async def randd(self, ctx, p: str):
        """Random(float) 1.0~x"""
        p = float(eval(p))
        if p>1.0:
            await ctx.send(random.uniform(1.0, p))
        else:
            await ctx.send(random.uniform(p, 1.0))

#---------------------------------------------------------- B系
class B(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='Bを連続送信します')
    async def BLOOP(self, ctx, times: int):
        """BLOOP number<=11"""
        if times > 12 :
            await ctx.send('too B!')
            return
        for _ in range(times):
            await ctx.send('B')
    @commands.group(description='greet, hello, help, block')
    # async def B(self, ctx, swit: str, swit2: str):
    async def B(self, ctx):
        """B + (greet / sysinfo / hello / block / typing)"""
        if ctx.invoked_subcommand is None:
            await ctx.send('B!')
    @B.command()
    async def greet(self, ctx):
        await ctx.send('こんにちは！ BBBot('+VERSION+')だよ。\nよろしくね')
    @B.command()
    async def sysinfo(self, ctx):
        ipInfo = 'IP :'+socket.gethostname()+': '+socket.gethostbyname(socket.gethostname())
        platInfo = 'OS : '+platform.platform()
        cpuInfo = 'CPU: '+cpuid.cpu_name()
        #cpuInfo = 'CPU: ['+str(psutil.cpu_count(logical=False))+'C '+str(psutil.cpu_count())+'T]'
        memInfo = 'MEM: '+str('{:.2f}'.format(psutil.virtual_memory().used/(1024*1024)))+'MB / '\
            +str('{:.2f}'.format(psutil.virtual_memory().total/(1024*1024)))+'MB'
        await ctx.send(ipInfo+"\n"+platInfo+"\n"+cpuInfo+"\n"+memInfo)
    @B.command()
    async def hello(self, ctx):
        await ctx.send('Hello B!')
    @B.command()
    async def block(self, ctx):
        await ctx.send('□□□□□□□□\n□■■■■□□□\n□■□□□■□□\n□■□□□■□□\n□■■■■□□□\n□■□□□■□□\n□■□□□□■□\n□■□□□□■□\n□■■■■■□□\n□□□□□□□□')
    @B.command()
    async def ping(self, ctx):
        await ctx.send(f"{bot.latency*1000}ms")
    @B.command()
    async def typing(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(10)
            ctx.typing()
            await ctx.send('B')
    @B.command()
    async def hattori(self, ctx, *tx:str):
        """ htr """
        txx = ' '.join(tx)
        # mChannel = bot.get_channel(MAIN_C)
        if 'end' in txx.lower():
            await ctx.send(HTRE_LIST[random.randrange(len(HTRE_LIST))])
        elif 'd' in txx.lower():
            await ctx.send(HTRD_LIST[random.randrange(len(HTRD_LIST))])
        else:
            await ctx.send(HTR_LIST[random.randrange(len(HTR_LIST))])
            
    # @B.command()
    # async def morning_call(self, ctx):
    #     """強制モーニングコールが行われる"""
    #     vChannel = bot.get_channel(VOICE_C)
    #     user = bot.fetch_user(HA) # get user from id
    #     await ctx.send(user)
    #     await user.move_to(vChannel)
    #     await vChannel.connect()
    #     VoiceChat.v_music(self, ctx, M_CALL)


#---------------------------------------------------------- 画像系
class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='melt picture')
    async def melt(self, ctx):
        """melt picture"""
        await Image.get_pic(self, ctx, 'https://dic.nicovideo.jp/oekaki/674964.png', 'melt.png')
    @commands.command(description='abya picture')
    async def abya(self, ctx):
        """abya picture"""
        await Image.get_pic(self, ctx, 'https://livedoor.blogimg.jp/mn726/imgs/0/3/03812153.jpg', 'abya.png')
    @commands.command(description='shiran kedo~ picture')
    async def shiran(self, ctx):
        """shiran kedo~ picture"""
        await Image.get_pic(self, ctx, 'https://pbs.twimg.com/media/DoGwbj0UwAALenI.jpg', 'shiran.jpg')
    @commands.command(description='party parrot GIF')
    async def party(self, ctx):
        """party parrot GIF"""
        await Image.get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/705099416083890281/766528750456012841/parrot.gif', 'party_parrot.gif')
    @commands.command(description='B picture')
    async def b_pic(self, ctx):
        """B picture"""
        await Image.get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/705099416083890281/766668684188975114/letter-b-clipart-158558-5546542.jpg', 'b_picture.jpg')
    @commands.command(description='gaming presentation GIF')
    async def presen(self, ctx):
        """gaming presentation GIF"""
        await Image.get_pic(self, ctx, 'https://cdn.discordapp.com/attachments/733937061199085610/768300192818135040/GPW.gif', 'gaming_presentation.gif')

    @commands.command(description='send photo')
    async def b_img(self, ctx, url: str, file_name: str):
        """b_img url file_name"""
        await Image.get_pic(self, ctx, url, file_name)

    async def get_pic(self, ctx, url: str, file_name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send('server error... b')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, file_name))


#---------------------------------------------------------- AI系
class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='a3rt AI TalkAPI')
    async def ai(self, ctx, talk: str):
        """a3rt AI TalkAPI"""
        data = urllib.parse.urlencode({"apikey":A3RT_KEY, "query":talk}).encode('utf-8')
        request = urllib.request.Request(A3RT_URI, data)
        res = urllib.request.urlopen(request)
        json_load = json.load(res)
        # await ctx.send('精度:'+str(json_load['results'][0]['perplexity'])+"\n"+json_load['results'][0]['reply'])
        await ctx.send(json_load['results'][0]['reply'])

#---------------------------------------------------------- youtube-dl
class Youtube(commands.Cog):
    ytdl_opts = {
        'format' : 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }
    # ytdl = youtube_dl.YoutubeDL(ytdl_opts)
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='youtube-dl audio only')
    async def ydl(self, ctx, url: str):
        """youtube-dl audio only [ org / max 8MB ]"""
        if 'soundcloud' in urllib.parse.urlparse(url).netloc: # soundcloud
            await self.ydl_m4a(ctx, url)
        else: # youtube (or niconico)
            filename = await self.ydl_proc(ctx, url, self.ytdl_opts)
            await self.ydl_send(ctx, filename)

    @commands.command(description='youtube-dl audio mp3')
    async def ydl_mp3(self, ctx, url: str):
        """youtube-dl audio only [ mp3 / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        #await self.ydl_proc(self, ctx, url, (self.ytdl_opts | setOpt)) # Python 3.9+
        filename = await self.ydl_proc(ctx, url, dict(self.ytdl_opts, **setOpt))
        await self.ydl_send(ctx, filename)
        # await ctx.send(json.dumps(self.ytdl_opts | setOpt)) #Debug

    @commands.command(description='youtube-dl audio m4a')
    async def ydl_m4a(self, ctx, url: str):
        """youtube-dl audio only [ m4a / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }
        #await self.ydl_proc(ctx, url, (self.ytdl_opts | setOpt)) # Python 3.9+
        filename = await self.ydl_proc(ctx, url, dict(self.ytdl_opts, **setOpt))
        await self.ydl_send(ctx, filename)
        # await ctx.send(json.dumps(self.ytdl_opts | setOpt)) #Debug

    @commands.command(description='youtube-dl audio aac')
    async def ydl_aac(self, ctx, url: str):
        """youtube-dl audio only [ aac / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
            }]
        }
        #await self.ydl_proc(ctx, url, (self.ytdl_opts | setOpt)) # Python 3.9+
        filename = await self.ydl_proc(ctx, url, dict(self.ytdl_opts, **setOpt))
        await self.ydl_send(ctx, filename)
        # await ctx.send(json.dumps(self.ytdl_opts | setOpt)) #Debug

    async def ydl_proc(self, ctx, url:str, ytdl_opts):
        if 'nico' in urllib.parse.urlparse(url).netloc: # niconico
            return await Youtube.ndl_proc(self, ctx, url)
        else: # youtube
            async with ctx.typing():
                try:
                    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        if 'postprocessors' in ytdl_opts:
                            filename = pathlib.PurePath(filename).stem + '.' + ytdl_opts['postprocessors'][0]['preferredcodec']
                        return filename
                except KeyError:
                    pass

    # niconico download
    async def ndl_proc(self, ctx, url:str):
        nico_path = pathlib.Path(str(url)).name
        nico = NicoNico(nico_path)
        nico_data = await nico.get_info()
        title = nico_data["video"]["title"] + '.mp4'
        await nico.download(title) # download & save
        nico.close()
        return await Youtube.ffmpeg(self, title, 'm4a')

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
        print(filename)
        try:
            with open(filename, 'rb') as fp:
                await ctx.send(file=discord.File(fp, filename))
        except discord.errors.HTTPException:
            await ctx.send('Error: File size is too large? [Max 8MB]\n')
        except:
            await ctx.send('Error: Unknown')
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            print(filename)


#---------------------------------------------------------- Discord_VoiceChat
class VoiceChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.now = None # now playing
        self.volume = 1.0
        self.inf_play = False # infinity play music

    @commands.command(description='Discord_VoiceChat Connect')
    async def v_connect(self, ctx):
        """Voice Connect"""
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(description='Discord_VoiceChat Disconnect')
    async def v_disconnect(self, ctx):
        """Voice Disconnect"""
        await ctx.voice_client.disconnect()

    @commands.command(description='Discord_VoiceChat TTS')
    async def v_boice(self, ctx, *tx:str):
        """Voice TTS (Japanese)"""
        await VoiceChat.make_tts(self, ctx, tx, 'ja', 1)

    @commands.command(description='same as v_boice')
    async def v_voice(self, ctx, *tx:str):
        """same as v_boice"""
        tx = ' '.join(tx)
        await VoiceChat.v_boice(self, ctx, tx)

    @commands.command(description='Discord_VoiceChat TTS EN')
    async def v_boice_en(self, ctx, *tx:str):
        """Voice TTS EN (English)"""
        await VoiceChat.make_tts(self, ctx, tx, 'en', 0)

    @commands.command(description='same as v_boice_en')
    async def v_voice_en(self, ctx, *tx:str):
        """same as v_boice_en"""
        tx = ' '.join(tx)
        await VoiceChat.v_boice_en(self, ctx, tx)

    @commands.command(description='play music')
    async def v_music(self, ctx, tx:str):
        """play music. (b = random, b_loop = random&loop)"""
        ytdl_opts = {
            'format' : 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        await VoiceChat.v_connect(self, ctx) # 接続確認
        self.inf_play = False # infiniry play: off
        if tx.lower() == 'stop' and self.now != None:
            self.now.stop()
            self.now = None

        elif tx.lower() == 'b': # random play!
            if self.now != None:
                self.now.stop()
                self.now = None
            music, sagyou_music = my_music.get_my_music()

            brand_n = list(music)[random.randint(0,int(len(music))-1)]
            brand = music[brand_n]
            mm = brand[random.randint(0,int(len(brand))-1)]

            filename = await Youtube.ydl_proc(self, ctx, mm['url'], ytdl_opts)
            await ctx.send(f'`{brand_n}` - `{mm["title"]}`')
            await VoiceChat.voice_send(self, ctx, filename)

        elif tx.lower() == 'b_loop': # infinity random play!
            if self.now != None:
                self.now.stop()
                self.now = None

            self.inf_play = True # infiniry play: on
            music, sagyou_music = my_music.get_my_music()
            while self.inf_play:
                brand_n = list(music)[random.randint(0,int(len(music))-1)]
                brand = music[brand_n]
                mm = brand[random.randint(0,int(len(brand))-1)]

                filename = await Youtube.ydl_proc(self, ctx, mm['url'], ytdl_opts)
                if not filename: continue
                await ctx.send(f'`{brand_n}` - `{mm["title"]}`')
                await VoiceChat.voice_send(self, ctx, filename)

        else:
            try: # try connect url
                f = urllib.request.urlopen(tx)
                f.close()
            except: return False

            if self.now != None:
                self.now.stop()
                self.now = None

            filename = await Youtube.ydl_proc(self, ctx, tx, ytdl_opts)
            await VoiceChat.voice_send(self, ctx, filename)

    @commands.command(description='play music + kawaii_voice_gtts.music_pack1')
    async def v_music_pack1(self, ctx, tx:str):
        """play music + kawaii_voice_gtts.music_pack1"""
        try: # try connect url
            f = urllib.request.urlopen(tx)
            f.close()
        except: return False

        ytdl_opts = {
            'format' : 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        self.now.stop()
        self.now = None
        filename = await Youtube.ydl_proc(self, ctx, tx, ytdl_opts)
        imouto = kawaii_voice_gtts.kawaii_voice(filename)
        imouto = imouto.music_pack1()
        imouto.audio.export(filename, 'mp3')
        await VoiceChat.voice_send(self, ctx, filename)

    async def make_tts(self, ctx, text, lg, k_option): # text=text, lg=language, k_option=kawaii_voice_gtts(0=false, 1=true)
        voice_client = ctx.message.guild.voice_client
        text = ' '.join(text)
        pool = string.ascii_letters + string.digits
        randm = ''.join(random.choice(pool) for i in range(16))
        filename = str(randm) + ".mp3"
        gTTS(str(text), lang=lg).save(filename)

        if k_option == 1:
            imouto = kawaii_voice_gtts.kawaii_voice(filename)
            imouto = imouto.pitch(0.4)
            imouto.audio.export(filename, 'mp3')

        if not voice_client: # join voice channel
            await ctx.author.voice.channel.connect()
        await VoiceChat.voice_send(self, ctx, filename)

    async def voice_send(self, ctx, filename):
        if os.path.exists(filename):
            if self.volume == 1.0: audio_source = discord.FFmpegPCMAudio(filename)
            else: audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), volume=self.volume)

            self.now = ctx.voice_client
            self.now.play(audio_source) # 再生
            while ctx.guild.voice_client.is_playing():
                await asyncio.sleep(1)
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
        await ctx.send('volume : '+str(self.volume))

    @commands.command(description='Channel member list')
    async def v_list(self, ctx):
        """Channel member list"""
        channel = ctx.author.voice.channel
        out = ''
        cnt = 1
        for ch in channel.guild.voice_channels:
            for member in ch.members:
                out += str(cnt) +' | '+ str(member) + '\n'
                cnt += 1
            #     await member.move_to(None)
        await ctx.send('```py\n'+out+'```')

    @commands.command(description='voice mute')
    async def v_mute(self, ctx, no):
        """voice mute. (b = all)"""
        channel = ctx.author.voice.channel
        if str(no).lower() == 'b': # 全員
            cnt = 0
            for ch in channel.guild.voice_channels:
                await ch.members[cnt].edit(mute = True)
                cnt += 1
        else: # 通常のミュート
            try:
                no = int(no)
                if no <= 0: return
            except: return
            for ch in channel.guild.voice_channels:
                if len(ch.members)-1 < no: return
                await ch.members[no-1].edit(mute = True)

    @commands.command(description='voice unmute')
    async def v_unmute(self, ctx, no):
        """voice unmute. (b = all)"""
        channel = ctx.author.voice.channel
        if str(no).lower() == 'b': # 全員
            cnt = 0
            for ch in channel.guild.voice_channels:
                await ch.members[cnt].edit(mute = False)
                cnt += 1
        else: # 通常のアンミュート
            try:
                if int(no) <= 0: return
            except: return
            for ch in channel.guild.voice_channels:
                if len(ch.members)-1 < no: return
                await ch.members[no-1].edit(mute = False)

    @commands.command(description='Discord_VoiceChat ALL D')
    async def v_bd(self, ctx):
        """Voice ALL D"""
        channel = ctx.author.voice.channel
        for ch in channel.guild.voice_channels:
            for member in ch.members:
                await member.move_to(None)


#---------------------------------------------------------- ASCII Encode
class Encode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='ASCII Encode')
    async def asc_enc(self, ctx, *text:str):
        """ASCII Encode"""
        text = ' '.join(text)
        send = ''
        for i in range(len(text)):
            send += ' ' + str(ord(text[i]))
        await ctx.send(send)

    @commands.command(description='ASCII Decode')
    async def asc_dec(self, ctx, *text:int):
        """ASCII Decode"""
        send = ''
        for i in range(len(text)):
            send += chr(text[i])
        await ctx.send(send)

#---------------------------------------------------------- GoogleTranslate
class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='Translate en -> ja')
    async def trans(self, ctx, *text):
        """Translate  English -> Japanese"""
        gReq = '?text='+str(' '.join(text))+'&source=en&target=ja'
        await Translate.transA(self, ctx, GoogleTranslateAPP_URL+gReq)

    @commands.command(description='Translate ja -> en')
    async def transJ(self, ctx, *text):
        """Translate Japanese -> English"""
        gReq = '?text='+str(' '.join(text))+'&source=ja&target=en'
        await Translate.transA(self, ctx, GoogleTranslateAPP_URL+gReq)

    async def transA(self, ctx, uri:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as res:
                if res.status == 200:
                    res_json = await res.json()
                    await ctx.send(res_json['res'])

#---------------------------------------------------------- Timer
class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='Timer (s)')
    async def timer(self, ctx, time_set:float):
        """Timer (s)"""
        mention = str(ctx.message.author.mention)
        dest = await ctx.send("Ready!")
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

        dest = await ctx.send("Ready!")
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
        self._last_member = None

    @commands.command(description='Exec BrainF*ck')
    async def bf(self, ctx, *tx:str):
        """Exec BrainF*ck"""
        tx = ''.join(tx)
        bfc = brainfuck.BrainFuck(tx, 0).bf()
        await ctx.send(bfc.out_asc)

    @commands.command(description='Debug BrainF*ck')
    async def bf_debug(self, ctx, *tx:str):
        """Debug BrainF*ck"""
        tx = ''.join(tx)
        bfc = brainfuck.BrainFuck(tx, 4).bf()
        # if len(bfc.debug) > 2000:
        await ctx.send(bfc.debug)

#---------------------------------------------------------- URL
class URL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='Generate Shorter URL')
    async def url_short(self, ctx, tx:str):
        """Generate shorter url"""
        await ctx.send(Shortener().tinyurl.short(tx))

    @commands.command(description='Restore the shortened URL')
    async def url_expand(self, ctx, tx:str):
        """Restore the shortened URL"""
        await ctx.send(Shortener().tinyurl.expand(tx))

    @commands.command(description='URL encode')
    async def url_enc(self, ctx, *tx:str):
        """URL encode"""
        s = ' '.join(tx)
        await ctx.send(urllib.parse.quote(s))

    @commands.command(description='URL decode')
    async def url_dec(self, ctx, *tx:str):
        """URL decode"""
        s = ' '.join(tx)
        await ctx.send(urllib.parse.unquote(s))

#---------------------------------------------------------- Slash
class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx:SlashContext):
        await ctx.send(f"{bot.latency*1000}ms")

    @cog_ext.cog_slash(name="hattori")
    async def hattori(self, ctx):
        await B.hattori(self, ctx)

    @cog_ext.cog_slash(name="v_connect")
    async def v_connect(self, ctx):
        await VoiceChat.v_connect(self, ctx)

    @cog_ext.cog_slash(name="v_disconnect")
    async def v_disconnect(self, ctx):
        await VoiceChat.v_disconnect(self, ctx)

    @cog_ext.cog_slash(name="v_voice_en")
    async def v_voice_en(self, ctx, *tx):
        tx = ' '.join(tx)
        await VoiceChat.v_boice_en(self, ctx, tx)

    @cog_ext.cog_slash(name="v_bd")
    async def v_bd(self, ctx):
        await VoiceChat.v_bd(self, ctx)

    @cog_ext.cog_slash(name="v_volume")
    async def v_volume(self, ctx, volume:str):
        await VoiceChat.v_volume(self, ctx, volume)

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
bot.run(TOKEN)
