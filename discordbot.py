# make requirements.txt command -> (myenv)$ pip freeze > requirements.txt
# Video and audio are file-like objects.

# This Discord bot uses PyNaCl & FFmpeg in VoiceChat class.
# ver1.4.0 of PyNaCl requires python 2.7, 3.5 - 3.8. (It did not work with ptyhon 3.9.3).


from __future__ import unicode_literals

import my_key # get my api keys

import os
import io
import math
import random
import string
import aiohttp #画像転送系
# import requests #req
import urllib.request
import urllib.parse
import json
import discord
from discord.ext import commands
# from discord_slash import SlashCommand
import random
import youtube_dl
import socket
import platform
import psutil
import cpuid
import time
import asyncio
import pathlib
from gtts import gTTS
from pyshorteners import Shortener


VERSION='v2.4.6'

TOKEN, A3RT_URI, A3RT_KEY, GoogleTranslateAPP_URL,\
    LOG_C, MAIN_C, VOICE_C = my_key.get_keys()

P2PEQ_URI='https://api.p2pquake.net/v1/human-readable'
# P2PEQ_URI='http://localhost:1011/p2p_ex/'
P2PEQ_INT=5 # GET interval (s)
P2PEW_NMIN=40 # Notification minimum earthquake scale
P2PEW_NMIN_LOG=20 # Notification minimum earthquake scale (log)

UP_SERVER = [ # wake up server uri
    '',
    '',
    ]
UP_SERVER_INT = 5 # up interval (min)

description = '''BさんのBBBot (v2.4.6)'''
bot = commands.Bot(command_prefix='?', description=description)
#----------------------------------------------------------

# 起動時に動作する処理
@bot.event
async def on_ready():
    # ログイン通知
    print(bot.user.name + ' is logged in.')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="B", emoji="🍝"))
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
        await lChannel.send("```\n@"+str(message.author.name)+"\n"+str(message.content)+" ```")
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
                                    and len(str(res_json[i]['earthquake']['maxScale'])) >= 1\
                                    and int(res_json[i]['earthquake']['maxScale']) >= P2PEW_NMIN \
                                    and res_json[i]['earthquake']['domesticTsunami'] != "Checking" :
                                        res_log  = res_json[i]
                                        await mChannel.send(await EqCheck.castRes(self, res_json, i))
                                        await lChannel.send(await EqCheck.castRes(self,res_json, i))
                                        # await lChannel.send(res_json)
                                    elif res_log != res_json[i] \
                                    and len(str(res_json[i]['earthquake']['maxScale'])) >= 1\
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
        lChannel = bot.get_channel(LOG_C)
        while True:
            # await lChannel.send('up server')
            try:
                for i in UP_SERVER:
                    req = urllib.request.Request(i)
                    with urllib.request.urlopen(req) as res:
                        body = res.read()
            except urllib.error.URLError as err:
<<<<<<< Updated upstream
                print(err.reason)
=======
                # print(err.reason)
>>>>>>> Stashed changes

            await asyncio.sleep(60*UP_SERVER_INT)


#---------------------------------------------------------- 計算系
class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='計算 Eval')
    # Evalなので攻撃しないでください。
    async def calc(self, ctx, inc: str):
        """Calc number Eval"""
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
        for i in range(times):
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
    async def typing(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(10)
            ctx.typing()
            await ctx.send('B')
    @B.command()
    async def hattori(self, ctx):
        mChannel = bot.get_channel(MAIN_C)
        await mChannel.send('ﾊｯﾄﾘｨ-')


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
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
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
    @commands.command(description='youtube-dl audio only')
    async def ydl(self, ctx, url: str):
        """youtube-dl audio only [ org / max 8MB ]"""
        filename = await Youtube.ydl_proc(self, ctx, url, Youtube.ytdl_opts)
        await Youtube.ydl_send(self, ctx, filename)

    @commands.command(description='youtube-dl audio mp3')
    async def ydl_m(self, ctx, url: str):
        """youtube-dl audio only [ mp3 / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        #await Youtube.ydl_proc(self, ctx, url, (Youtube.ytdl_opts | setOpt)) # Python 3.9+
        filename = await Youtube.ydl_proc(self, ctx, url, dict(Youtube.ytdl_opts, **setOpt))
        await Youtube.ydl_send(self, ctx, filename)
        # await ctx.send(json.dumps(Youtube.ytdl_opts | setOpt)) #Debug

    @commands.command(description='youtube-dl audio m4a')
    async def ydl_m4a(self, ctx, url: str):
        """youtube-dl audio only [ m4a / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }
        #await Youtube.ydl_proc(self, ctx, url, (Youtube.ytdl_opts | setOpt)) # Python 3.9+
        filename = await Youtube.ydl_proc(self, ctx, url, dict(Youtube.ytdl_opts, **setOpt))
        await Youtube.ydl_send(self, ctx, filename)
        # await ctx.send(json.dumps(Youtube.ytdl_opts | setOpt)) #Debug

    @commands.command(description='youtube-dl audio m4a 128kbps')
    async def ydl_m4a_min(self, ctx, url: str):
        """youtube-dl audio only [ m4a 128kbps / max 8MB ]"""
        setOpt = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                "preferredquality": "128"
            }]
        }
        #await Youtube.ydl_proc(self, ctx, url, (Youtube.ytdl_opts | setOpt)) # Python 3.9+
        filename = await Youtube.ydl_proc(self, ctx, url, dict(Youtube.ytdl_opts, **setOpt))
        await Youtube.ydl_send(self, ctx, filename)
        # await ctx.send(json.dumps(Youtube.ytdl_opts | setOpt)) #Debug

    async def ydl_proc(self, ctx, url:str, ytdl_opts):
        async with ctx.typing():
            with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                try:
                    filename = pathlib.PurePath(filename).stem + '.' + ytdl_opts['postprocessors'][0]['preferredcodec']
                except KeyError:
                    pass
                return filename

    async def ydl_send(self, ctx, filename):
        try:
            with open(filename, 'rb') as fp:
                await ctx.send(file=discord.File(fp, filename))
        except discord.errors.HTTPException:
            await ctx.send('Error: File size is too large? [Max 8MB]\nYou can use "?ydl_m4a_min" command!!\n')
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
        await VoiceChat.make_tts(self, ctx, tx, 'ja')

    @commands.command(description='same as v_boice')
    async def v_voice(self, ctx, *tx:str):
        """seme as v_boice"""
        tx = ' '.join(tx)
        await VoiceChat.v_boice(self, ctx, tx)

    @commands.command(description='Discord_VoiceChat TTS EN')
    async def v_boice_en(self, ctx, *tx:str):
        """Voice TTS EN (English)"""
        await VoiceChat.make_tts(self, ctx, tx, 'en')

    @commands.command(description='same as v_boice_en')
    async def v_voice_en(self, ctx, *tx:str):
        """seme as v_boice_en"""
        tx = ' '.join(tx)
        await VoiceChat.v_boice_en(self, ctx, tx)

    @commands.command(description='same as v_boice_en')
    async def v_music(self, ctx, tx:str):
        """seme as v_boice_en"""
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
        filename = await Youtube.ydl_proc(self, ctx, tx, ytdl_opts)
        await VoiceChat.voice_send(self, ctx, filename)


    async def make_tts(self, ctx, text, lg):
        voice_client = ctx.message.guild.voice_client
        text = ' '.join(text)
        pool = string.ascii_letters + string.digits
        randm = ''.join(random.choice(pool) for i in range(16))
        filename = str(randm) + ".mp3"
        gTTS(str(text), lang=lg).save(filename)

        if not voice_client: # join voice channel
            await ctx.author.voice.channel.connect()
        VoiceChat.voice_send(self, ctx, filename)

    async def voice_send(self, ctx, filename):
        if os.path.exists(filename):
            audio_source = discord.FFmpegPCMAudio(filename)
            ctx.voice_client.play(audio_source)
            while ctx.guild.voice_client.is_playing():
                await asyncio.sleep(1)
            os.remove(filename)
        

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
        lists=list(text)
        send = ''
        for w in lists:
            send = send + ' ' + str(ord(w))
        await ctx.send(send)

    @commands.command(description='ASCII Decode')
    async def asc_dec(self, ctx, *text:int):
        """ASCII Decode"""
        await ctx.send('{}'.format(len(text), ''.join(chr(text))))

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
    async def timer(self, ctx, time:int):
        """Timer (s)"""
        mention = str(ctx.message.author.mention)
        dest = await ctx.send("Ready!")
        while time > 0:
            time -= 1
            await asyncio.sleep(1)
            await dest.edit(content = f'{mention}'+" | left: "+str(time))
        await dest.edit(content = f'{mention}'+" | Time up!")

    @commands.command(description='pomodoro set, work(min), break(min)')
    async def pomodoro(self, ctx, *tset:int):
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
            time, time2 = time_, time2_ # reset time
            while time > 0: # work
                time -= 5
                await asyncio.sleep(5)
                await dest.edit(content = f'{mention}'+" | "+str(setCnt_ - setCnt + 1)+"/"+str(setCnt_)+" work left: "+ str(int(time/60)).zfill(2)+":"+str(int(time%60)).zfill(2))
            while time2 > 0: # break
                time2 -= 5
                await asyncio.sleep(5)
                await dest.edit(content = f'{mention}'+" | "+str(setCnt_ - setCnt + 1)+"/"+str(setCnt_)+" break left: "+ str(int(time2/60)).zfill(2)+":"+str(int(time2%60)).zfill(2))
            setCnt -= 1
        await dest.edit(content = f'{mention}'+" Good jobbb!\nRecord: cnt="+str(setCnt_)+", work: "+str(int(time_/60))+"(min) / break: "+str(int(time2_/60))+"(min)")

#---------------------------------------------------------- BrainF*ck
class BrainFuck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description='Exec BrainF*ck')
    async def bf(self, ctx, tx:str):
        """Exec BrainF*ck"""

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
# bot.add_cog(BrainFuck(bot))
bot.add_cog(URL(bot))
bot.run(TOKEN)
