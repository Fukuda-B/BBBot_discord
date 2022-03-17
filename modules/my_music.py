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
    music = open_yaml(f_name='./modules/adv_music.yaml')

    # 好みのやつ
    fav_music = open_yaml(f_name='./modules/fav_music.yaml')

    # 作業用
    sagyou_music = {}

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
