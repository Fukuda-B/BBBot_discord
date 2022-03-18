'''
    eq_check/eq_check.py
'''

import asyncio
import aiohttp
import datetime

class EqCheck(object):
    def __init__(self, bot, log_c, main_c):
        self.EQ_URI = 'http://www.kmoni.bosai.go.jp/webservice/hypo/eew/'
        # self.EQ_URI = 'http://localhost:3000/'
        self.EQ_INT = 2 # request interval (s)
        self.EQ_NMIN = 40 # Notification minimum earthquake scale

        # $res_log structure
        # {
        #   'report_id': {
        #       'discord_message_id':val,
        #       'report_num':val
        #   },
        #   'report_id': {
        #       ...
        #   },
        # }
        self.res_log_main = {} # Earthake report id list
        self.res_log_log = {}

        # Discord
        self.bot = bot
        self.lChannel = self.bot.get_channel(log_c) # logger discord channel
        self.mChannel = self.bot.get_channel(main_c) # main discord channel

    async def p2peq_check(self):
        while True:
            t_delta = datetime.timedelta(hours=9)
            jst = datetime.timezone(t_delta, 'JST')
            dt = datetime.datetime.now(jst)
            j_name = dt.strftime('%Y%m%d%H%M%S') + '.json'
            # j_name = ''
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.EQ_URI+j_name) as res:
                        if res.status == 200:
                            res_json = await res.json()
                            if res_json['result']['status'] == "success" and\
                                'alertflg' in res_json and\
                                len(res_json['report_id']) > 0 and\
                                res_json['is_training'] == False:
                                await self.report(res_json)
            except Exception as e:
                print(e)
            await asyncio.sleep(self.EQ_INT)

    async def report(self, json_data):
        scale_list = {
            '0': 0,
            '1': 10,
            '2': 20,
            '3': 30,
            '4': 40,
            '5弱': 45,
            '5強': 50,
            '6弱': 55,
            '6強': 60,
            '7': 70,
        }
        send_data = "```yaml\n"\
            + "Earthquake : " + str(json_data['report_time']) + "\n"\
            + "Place      : " + str(json_data['region_name'])\
            + " (N" + str(json_data['latitude']) + " E" + str(json_data['longitude']) + ")\n"\
            + "Depth      : " + str(json_data['depth']) + "\n"\
            + "MaxScale   : " + str(json_data['calcintensity']) + "\n"\
            + "Magnitude  : " + str(json_data['magunitude']) + "\n"\
            + "Update     : " + str(json_data['report_num']) + " / Final = " + str(json_data['is_final']) + "\n"\
            + "```"

        # main
        # print(scale_list[json_data['calcintensity']])
        if (json_data['calcintensity'] in scale_list): # 震度の変換ができるか
            if (scale_list[json_data['calcintensity']] >= self.EQ_NMIN): # 緊急地震速報(警報) の場合はメインチャンネルに通知
                if (json_data['report_id'] not in self.res_log_main):
                    res = await self.mChannel.send(send_data)
                    self.res_log_main[json_data['report_id']] = {
                        "discord_message_id": res,
                        "report_num": json_data['report_num'],
                    }
                elif json_data['report_num'] != self.res_log_main[json_data['report_id']]['report_num']:
                        res = self.res_log_main[json_data['report_id']]['discord_message_id']
                        await res.edit(send_data)
                        self.res_log_main[json_data['report_id']]['report_num'] = json_data['report_num']

        # logger
        if (json_data['report_id'] not in self.res_log_log):
            res = await self.lChannel.send(send_data) # 緊急地震速報(予報) の場合はログチャンネルに通知
            self.res_log_log[json_data['report_id']] = {
                "discord_message_id": res,
                "report_num": json_data['report_num'],
            }
        elif json_data['report_num'] != self.res_log_log[json_data['report_id']]['report_num']:
                res = self.res_log_log[json_data['report_id']]['discord_message_id']
                await res.edit(send_data)
                self.res_log_log[json_data['report_id']]['report_num'] = json_data['report_num']
