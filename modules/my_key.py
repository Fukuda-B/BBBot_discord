# API keys are separated from v2.3.3
def get_keys():
    TOKEN=''

    A3RT_URI='https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk'
    A3RT_KEY=''

    GoogleTranslateAPP_URL=''

    LOG_C=  # LOGS Channel
    # MAIN_C= # SEND Channel (本番用)
    MAIN_C= # SEND Channel (試験用)
    VOICE_C= # VOICE Channel (試験用)
    HA = # sleeping people
    BBB = # 管理者
    VC_C = [] # 配信中毒者

    UP_SERVER = [ # wake up server uri
        '',
        '',
    ]

    M_CALL = ''

    return TOKEN, A3RT_URI, A3RT_KEY, GoogleTranslateAPP_URL, LOG_C, MAIN_C, VOICE_C, HA, BBB, VC_C, UP_SERVER, M_CALL
