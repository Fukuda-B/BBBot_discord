# 地震の通知用モジュール

import aiohttp
import urllib
import asyncio

P2PEQ_URI = 'https://api.p2pquake.net/v1/human-readable'
# P2PEQ_URI = 'http://localhost:1011/p2p_ex/'
P2PEQ_INT = 5 # GET interval (s)
P2PEW_NMIN = 40 # Notification minimum earthquake scale
P2PEW_NMIN_LOG = 20 # Notification minimum earthquake scale (logger)

class EqCheck:
    def __init__(self, bot, log_c, main_c):
        self.bot = bot
        self.log_c = log_c
        self.main_c = main_c

    async def p2peq_check(self):
        # req = urllib.request.Request(P2PEQ_URI)
        res_log = [] # Earthquake log
        lChannel = self.bot.get_channel(self.log_c)
        mChannel = self.bot.get_channel(self.main_c)

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
                                            await lChannel.send(await EqCheck.castRes(self, res_json, i))
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
