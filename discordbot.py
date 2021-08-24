# make requirements.txt command -> (myenv)$ pip freeze > requirements.txt
# Video and audio are file-like objects.

# This Discord bot uses PyNaCl & FFmpeg in VoiceChat class.

# pip update
# powershell: pip3 install --upgrade ((pip3 freeze) -replace '==.+','')
# https://www.yukkuriikouze.com/2019/07/12/3105/


from __future__ import unicode_literals

from discord import channel

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

VERSION='v2.6.4 beta'

TOKEN, A3RT_URI, A3RT_KEY, GoogleTranslateAPP_URL,\
    LOG_C, MAIN_C, VOICE_C, HA, UP_SERVER,\
    M_CALL = my_key.get_keys()

HTR_LIST = htr.get_hattori()
HTRE_LIST = htr_end.end_hattori()
HTRD_LIST = htr_dead.dead_hattori()

P2PEQ_URI = 'https://api.p2pquake.net/v1/human-readable'
# P2PEQ_URI = 'http://localhost:1011/p2p_ex/'
P2PEQ_INT = 5 # GET interval (s)
P2PEW_NMIN = 40 # Notification minimum earthquake scale
P2PEW_NMIN_LOG = 20 # Notification minimum earthquake scale (logger)

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
    # await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="BBBot "+VERSION, emoji="🍝"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="BBBot "+VERSION, emoji="🍝"))
    # await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="BBBot "+VERSION))
    lChannel = bot.get_channel(LOG_C)
    await lChannel.send('BBBot is Ready! ' + VERSION)

    # 非同期並行処理
    await asyncio.gather(
        EqCheck(bot).p2peq_check(),
        UpServer(bot).up_server(),
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
                                    try:
                                        if len(res_log) <= 0: # 初回の処理
                                            res_log  = res_json[i]
                                        elif res_log != res_json[i] \
                                        and type(res_json[i]['earthquake']['maxScale']) != type(None)\
                                        and int(res_json[i]['earthquake']['maxScale']) >= P2PEW_NMIN \
                                        and res_json[i]['earthquake']['domesticTsunami'] != "Checking" :
                                            res_log  = res_json[i]
                                            await mChannel.send(await EqCheck.castRes(self, res_json, i))
                                            await lChannel.send(await EqCheck.castRes(self,res_json, i))
                                            # await lChannel.send(res_json)
                                        elif res_log != res_json[i] \
                                        and type(res_json[i]['earthquake']['maxScale']) != type(None)\
                                        and int(res_json[i]['earthquake']['maxScale']) >= P2PEW_NMIN_LOG:
                                            await lChannel.send(await EqCheck.castRes(self,res_json, i))
                                            res_log  = res_json[i]
                                        break
                                    except Exception as e:
                                        print(e)
                                        continue

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
            except Exception as e:
                print(e)
            # except urllib.error.URLError as err:
            #     print(err.reason)
            #     pass

            await asyncio.sleep(60*UP_SERVER_INT)

#---------------------------------------------------------- 計算系
class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # @commands.command(description='計算 Eval')
    # # Evalなので攻撃しないでください。
    # async def calc(self, ctx, *inc: str):
    #     """Calc number Eval"""
    #     inc = ''.join(inc)
    #     inc = re.sub(r"[\u3000 \t]", "", inc)
    #     await Basic.send(self, ctx, eval(inc))
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
        p = float(eval(p))
        if p == 0.0:
            await Basic.send(self, ctx, 0.0)
        else:
            await Basic.send(self, ctx, -p*math.log2(p))
    @commands.command(description='エントロピー関数計算H()')
    async def ent(self, ctx, p: str):
        """EntropyFunc H(p)"""
        p = float(eval(p))
        if p == 0.0:
            await Basic.send(self, ctx, 0.0)
        else:
            await Basic.send(self, ctx, -p*math.log2(p)-(1-p)*math.log2(1-p))
    @commands.command(description='乱数(int) 1~x')
    async def rand(self, ctx, p: str):
        """Random(int) 1~x"""
        p = int(eval(p))
        if p>1:
            await Basic.send(self, ctx, random.randint(1, p))
        else:
            await Basic.send(self, ctx, random.randint(p, 1))
    @commands.command(description='乱数(float)) 1.0~x')
    async def randd(self, ctx, p: str):
        """Random(float) 1.0~x"""
        p = float(eval(p))
        if p>1.0:
            await Basic.send(self, ctx, random.uniform(1.0, p))
        else:
            await Basic.send(self, ctx, random.uniform(p, 1.0))

#---------------------------------------------------------- B系
class B(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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
    @commands.command(description='maji yabakune')
    async def majiyaba(self, ctx):
        """maji yabakune"""
        await Image.get_pic(self, ctx, 'https://pbs.twimg.com/media/C34X4w0UcAEyKW-.jpg', 'majiyaba.jpg')

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
        self._last_member = None

    @commands.command(description='a3rt AI TalkAPI')
    async def ai(self, ctx, talk: str):
        """a3rt AI TalkAPI"""
        data = urllib.parse.urlencode({"apikey":A3RT_KEY, "query":talk}).encode('utf-8')
        request = urllib.request.Request(A3RT_URI, data)
        res = urllib.request.urlopen(request)
        json_load = json.load(res)
        # await Basic.send(self, ctx, '精度:'+str(json_load['results'][0]['perplexity'])+"\n"+json_load['results'][0]['reply'])
        await Basic.send(self, ctx, json_load['results'][0]['reply'])

#---------------------------------------------------------- youtube-dl
class Youtube(commands.Cog):
    ytdl_opts = {
        'format' : 'bestaudio/best',
        # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'outtmpl': '%(title)s.%(id)s.%(ext)s',
        'restrictfilenames': True,
        # 'noplaylist': True, # allow playlist
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
            for i in range(len(filename)):
                await self.ydl_send(ctx, filename[i])

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
            await self.ydl_send(ctx, filename[i])

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
            await self.ydl_send(ctx, filename[i])
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
            await self.ydl_send(ctx, filename[i])
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
                        plist.append(pre_info['entries'][i]['webpage_url'])
                    return plist
                else:
                    return [url]
            except:
                return False

    async def ydl_proc(self, ctx, url:str, ytdl_opts):
        """" download video & return filenames(list) """
        if 'nico' in urllib.parse.urlparse(url).netloc: # niconico
            return await Youtube.ndl_proc(self, ctx, url)
        else: # youtube
            async with ctx.typing():
                try:
                    # 事前に情報取得
                    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                        pre_info = ydl.extract_info(url, download=False)
                    if 'entries' in pre_info:
                        # playlist (multiple video)
                        video = pre_info['entries']
                        filenames = []
                        for i, item in enumerate(video):
                            with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                                info = ydl.extract_info(pre_info['entries'][i]['webpage_url'], download=True)
                                filename = ydl.prepare_filename(info)
                                if 'postprocessors' in ytdl_opts:
                                    filename = pathlib.PurePath(filename).stem + '.' + ytdl_opts['postprocessors'][0]['preferredcodec']
                                filenames.append(filename)
                        return filenames
                    else:
                        # single video
                        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            filename = ydl.prepare_filename(info)
                            if 'postprocessors' in ytdl_opts:
                                filename = pathlib.PurePath(filename).stem + '.' + ytdl_opts['postprocessors'][0]['preferredcodec']
                            return [filename]
                except:
                    await Basic.send(self, ctx, 'Error: Youtube.ydl_proc')
                    return False

    # niconico download
    async def ndl_proc(self, ctx, url:str):
        try:
            nico_path = pathlib.Path(str(url)).name
            nico = NicoNico(nico_path)
            nico_data = await nico.get_info()
            title = nico_data["video"]["title"] + '.mp4'
            await nico.download(title) # download & save
            nico.close()
            return await Youtube.ffmpeg(self, title, 'm4a')
        except:
            return False

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
        except discord.errors.HTTPException:
            await Basic.send(self, ctx, 'Error: File size is too large? [Max 8MB]\n')
        except Exception as e:
            print(e)
            await Basic.send(self, ctx, 'Error: Unknown')
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
        self.queue = [] # music queue ['now play', 'next', '...'] (url)
        self.state = False # continue to play
        self.nightcore = False # nightcore effect
        self.bassboost = False # bassboost effect

    @commands.command(description='Discord_VoiceChat Connect')
    async def v_connect(self, ctx):
        """Voice Connect"""
        channel = ctx.author.voice.channel
        if (not ctx.author.voice) or (not ctx.author.voice.channel): # ボイスチャンネルに入っていない
            await Basic.send(self, ctx, 'You need to be in the voice channel first.')
            return
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

    @commands.group(description='play music (b/b_loop/stop/skip/queue/play)')
    async def v_music(self, ctx):
        """play music. (b/b_loop/stop/skip/queue/queue_del/play)"""
        self.ytdl_opts = {
            'format' : 'bestaudio/best',
            # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'outtmpl': '%(title)s.%(id)s.%(ext)s',
            'restrictfilenames': True,
            # 'noplaylist': True,
            'nocheckcertificate': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        await VoiceChat.v_connect(self, ctx) # 接続確認

        if ctx.invoked_subcommand is None: # サブコマンドがない場合
            self.state = False # auto play: off
            self.inf_play = False # stop inf play
            tx = str(ctx.message.content).split()[1] # サブコマンドではない場合、URLとして扱う
            if not tx: return
            try: # try connect url
                f = urllib.request.urlopen(tx)
                f.close()
            except: return False
            if self.now != None and self.state != True:
                self.now.stop()
                self.now = None

            plist = await Youtube.ydl_getc(self, ctx, tx, self.ytdl_opts)
            self.queue.extend(plist)
            if self.now == None and len(self.queue):
                if len(self.queue) == 1: # 1曲だけの場合
                    next_song_url = self.queue.pop(0)
                    [next_song_filename] = await Youtube.ydl_proc(self, ctx, next_song_url, self.ytdl_opts)
                    next_song_filename = await VoiceChat.effect(self, next_song_filename) # エフェクト
                    await VoiceChat.voice_send(self, ctx, next_song_filename)
                elif len(self.queue) > 0: # 複数曲の場合 (曲の表示等あり)
                    await Basic.send(self, ctx, str(len(plist))+" songs added")
                    await VoiceChat.play(self, ctx)

    @v_music.command(description='skip')
    async def skip(self, ctx):
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
        self.state = False # auto play: off
        if self.now != None:
            self.now.stop()
            self.now = None

    @v_music.command(description='random play!')
    async def b(self, ctx):
        self.state = False # auto play: off
        self.inf_play = False # stop inf play
        if self.now != None:
            self.now.stop()
            self.now = None
        music, sagyou_music = my_music.get_my_music()

        if len(music) == 1: brand_n = list(music)[0]
        else: brand_n = list(music)[random.randint(0,int(len(music))-1)]

        brand = music[brand_n]
        if len(brand) == 1: mm = brand[0]
        else: mm = brand[random.randint(0,int(len(brand))-1)]

        self.ytdl_opts['noplaylist'] = True
        filename_ = await Youtube.ydl_proc(self, ctx, mm['url'], self.ytdl_opts)
        if filename_:
            filename = filename_[0]
            filename = await VoiceChat.effect(self, filename) # エフェクト
            # await Basic.send(self, ctx, f'`{brand_n}` - `{mm["title"]}`')
            await Basic.send(self, ctx, f'```ini\n[TITLE] {brand_n} - {mm["title"]}\n[ URL ] {mm["url"]}```')
            await VoiceChat.voice_send(self, ctx, filename)

    @v_music.command(description='infinity random play!')
    async def b_loop(self, ctx):
        self.state = False # auto play: off
        if self.now != None:
            self.now.stop()
            self.now = None

        self.inf_play = True # infiniry play: on
        music, sagyou_music = my_music.get_my_music()
        while self.inf_play:
            brand_n = list(music)[random.randrange(len(music))]
            # brand_n = list(music)[random.randint(0,int(len(music)-1))]
            brand = music[brand_n]
            # mm = brand[random.randint(0,int(len(brand)-1))]
            mm = brand[random.randrange(len(brand))]

            self.ytdl_opts['noplaylist'] = True
            filename_ = await Youtube.ydl_proc(self, ctx, mm['url'], self.ytdl_opts)
            if not filename_ and self.now == None: # youtube_dl error
                # await Basic.send(self, ctx, 'Error: Youtube.ydl_proc')
                print('Error: Youtube.ydl_proc')
                continue
            elif self.now == None: # 正常
                # try:
                filename = filename_[0]
                filename = await VoiceChat.effect(self, filename) # エフェクト
                # await Basic.send(self, ctx, f'`{brand_n}` - `{mm["title"]}`')
                await Basic.send(self, ctx, f'```ini\n[TITLE] {brand_n} - {mm["title"]}\n[ URL ] {mm["url"]}```')
                await VoiceChat.voice_send(self, ctx, filename)
                # except:
                #     await Basic.send(self, ctx, 'Error: Youtube.voice_send')
            else: break

    @v_music.command(description='play')
    async def play(self, ctx):
        """ play queue """
        self.state = True
        while len(self.queue):
            if self.now == None:
                # try:
                next_song_url = self.queue.pop(0)
                [next_song_filename] = await Youtube.ydl_proc(self, ctx, next_song_url, self.ytdl_opts)
                next_song_filename = await VoiceChat.effect(self, next_song_filename) # エフェクト
                split_filename = os.path.basename(next_song_filename).split('.')
                split_filename.pop(len(split_filename)-1) # ファイルの拡張子を除く
                split_filename.pop(len(split_filename)-1) # youtube id を除く
                await Basic.send(self, ctx, f'```ini\n[TITLE] {"".join(split_filename)}\n[ URL ] {next_song_url}```')
                await VoiceChat.voice_send(self, ctx, next_song_filename)
                # except:
                #     await Basic.send(self, ctx, "Error: VoiceChat.play")
                #     continue
            if len(self.queue) <= 0 or not self.state:
                break

    @v_music.command(description='queue')
    async def queue(self, ctx):
        if len(self.queue) > 0:
            sd = '> | '+str(self.queue[0])+'\n'
            for i in range(1, len(self.queue)):
                sd += str(i)+' | '+str(self.queue[i])+'\n'
            await Basic.send(self, ctx, "```py\n"+sd+"```")
        else:
            await Basic.send(self, ctx, "queue = Null")

    @v_music.command(description='delete queue')
    async def del_queue(self, ctx):
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
        voice_client = ctx.message.guild.voice_client
        text = ' '.join(text)
        pool = string.ascii_letters + string.digits
        randm = ''.join(random.choice(pool) for _ in range(16))
        filename = str(randm) + ".mp3"
        gTTS(str(text), lang=lg).save(filename)

        if k_option == 1:
            imouto = kawaii_voice_gtts.kawaii_voice(filename)
            imouto = imouto.pitch(0.4)
            imouto.audio.export(filename, 'mp3')

        if not voice_client: # join voice channel
            await ctx.author.voice.channel.connect()
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
        if self.now != None:
            self.now.stop()
        if os.path.exists(filename): # ファイル存在確認
            if self.volume == 1.0: audio_source = discord.FFmpegPCMAudio(filename)
            else: audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), volume=self.volume)

            self.now = ctx.voice_client
            try:
                self.now.play(audio_source) # 再生
                while ctx.guild.voice_client.is_playing():
                    await asyncio.sleep(1)
            except Exception as e:
                print(e)
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
                    await Basic.send(self, ctx, res_json['res'])

#---------------------------------------------------------- Timer
class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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
        self._last_member = None

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
        self._last_member = None

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

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx:SlashContext):
        await Basic.send(self, ctx, f"{bot.latency*1000}ms")

    @cog_ext.cog_slash(name="hattori")
    async def hattori(self, ctx:SlashContext):
        await B.hattori(self, ctx)

    @cog_ext.cog_slash(name="v_connect")
    async def v_connect(self, ctx:SlashContext):
        await VoiceChat.v_connect(self, ctx)

    @cog_ext.cog_slash(name="v_disconnect")
    async def v_disconnect(self, ctx:SlashContext):
        await VoiceChat.v_disconnect(self, ctx)

    @cog_ext.cog_slash(name="v_voice_en")
    async def v_voice_en(self, ctx:SlashContext, *tx):
        tx = ' '.join(tx)
        await VoiceChat.v_boice_en(self, ctx, tx)

    @cog_ext.cog_slash(name="v_bd")
    async def v_bd(self, ctx:SlashContext):
        await VoiceChat.v_bd(self, ctx)

    @cog_ext.cog_slash(name="v_volume")
    async def v_volume(self, ctx:SlashContext, volume:str):
        await VoiceChat.v_volume(self, ctx, volume)

#---------------------------------------------------------- Basic
class Basic():
    def __init__(self, bot):
        self.bot = bot

    async def get_random(n):
        base = string.digits + string.ascii_lowercase + string.ascii_uppercase
        return str(''.join([random.choice(base) for _ in range(n)]))

    async def send(self, ctx, tx):
        """ 文字の送信 """
        if len(str(tx)) <= 2000: # 2000文字以下
            await ctx.send(str(tx))
        else:
            try:
                data = io.StringIO(str(tx))
                await ctx.send(file=discord.File(data, 'res.txt'))
            except Exception as e: # サイズ上限?
                print(e)
                await ctx.send('Error: Size limit has been exceeded?')

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
