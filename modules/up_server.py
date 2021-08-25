# サーバを活性化するモジュール

import urllib
import asyncio

class UpServer:
    def __init__(self, bot, log_c, up_server):
        self.bot = bot
        self.log_c = log_c
        self.up_server_list = up_server
        self.up_server_int = 5 # up interval (min)

    async def up_server(self):
        lChannel = self.bot.get_channel(self.log_c)
        while True:
            # await lChannel.send('up server')
            try:
                for i in self.up_server_list:
                    req = urllib.request.Request(i)
                    with urllib.request.urlopen(req):
                        pass
                    # with urllib.request.urlopen(req) as res:
                    #     pass
                    #     body = res.read()
            except urllib.error.URLError:
                # await lChannel.send('Error: urllib.error.URLError')
                pass
            except Exception as e:
                print(e)
                await lChannel.send(str(e))
            # except urllib.error.URLError as err:
            #     print(err.reason)
            #     pass

            await asyncio.sleep(60*self.up_server_int)
