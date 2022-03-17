# 好みのADV (PC, 他 / 美少女ゲーム) 曲
# 数が多いため、内部で異なるブランドの場合も同じブランドとする場合がある
# 非公式の場合は、コメントを書くこと
# オープニング等は、OPで省略
#
# 同会社でも別ブランドがある場合や、さらにそのサブブランドという位置付けのものもあるので難しい。姉妹ブランドやグループブランドなども。
# ブランドの詳細は https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%80%E3%83%AB%E3%83%88%E3%82%B2%E3%83%BC%E3%83%A0%E3%83%A1%E3%83%BC%E3%82%AB%E3%83%BC%E4%B8%80%E8%A6%A7
# 2021/12頃 更新

import random
import yaml

def open_yaml(f_name):
    """load yaml files"""
    try:
        with open(f_name, encoding='utf_8') as file:
            obj = yaml.safe_load(file)
            return obj
    except Exception as e:
        print(e)
        return False

def get_my_music():
    # 通常
    music = open_yaml(f_name='./modules/adv_music.yml')

    # 好みのやつ
    fav_music = open_yaml(f_name='./modules/fav_music.yml')

    # 作業用
    sagyou_music = {}

    # アリスソフト, みなとそふと, TYPE-MOON, 自宅すたじお,
    # May-Be SOFT -> ぱいタッチ！ OP
    # aries soft -> タラレバ ED
    # Cabbit -> キミへ贈る、ソラの花 OP
    # lantis -> ましろ色シンフォニー
    # Navel -> 月乙
    # 絶対☆大好き https://www.youtube.com/watch?v=YA5EioW0oLQ
    # leaf フルアニ, ToHeart2
    # ケロＱ / 枕 -> サクラノ詩
    # WillPlus/PULLTOP.. 系列
    # chien, unicorn, Navel, 
    # whitepowder -> lamunation!
    # rask -> Re:Lief
    # MOONSTONE, チュアブルソフト, studio-ege, 
    # GLacé / Galette, プラリネ, ILLUSIONI, 

    # akabei3 = [
    #     https://www.youtube.com/channel/UC-nhyMMGNXQQsXrdtDx3mSg
    # ]

    # Frontwing = [
    #     # https://www.youtube.com/channel/UCCaZwRx_HS61ZiNUrBdmDoA
    # ]

    # giga, PULLTOP, tyuaburu_soft, silkysplus, Lose, tone_works, SWEETTEA, palette_qualia, Campus, Key. QUINCE_SOFT
    # Galette, Navel, CUBE, sumikko_soft, Escu_de

    return music, fav_music, sagyou_music


def get_music():
    """get random music"""
    while True:
        music, fav_music, sagyou_music = get_my_music()
        if len(music) <= 0: break # 曲がない
        if len(music) == 1: brand_n = list(music)[0]
        else:
            rr = random.randint(0,int(len(music))-1)
            brand_n = list(music)[rr]
            # print(f'brand {rr} | {brand_n}')

        brand = music[brand_n]
        if len(brand) <= 0: continue # ブランドに曲がない
        if len(brand) == 1: mm = brand[0]
        else:
            rr = random.randint(0,int(len(brand))-1)
            mm = brand[rr]
            # print(f'mm {rr} | {mm}')
            break
    return brand_n, mm

def get_brand_music(brand_n):
    """get random music (select name)"""
    # print(brand_n)
    music, sagyou_music = get_my_music()
    if brand_n in music.keys() and len(music[brand_n]) > 0: # ブランド, 曲が存在する
        brand = music[brand_n]
        rr = random.randint(0, int(len(brand))-1)
        mm = brand[rr]
        return brand_n, mm
    else: return get_music()


def get_brand_list():
    """get brand list"""
    music, sagyou_music = get_my_music()
    brand_list = []
    for key in music.keys():
        brand_list.append(key)
    return brand_list

if __name__ == '__main__':
    for _ in range(100):
        print(get_music())
