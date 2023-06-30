import math, random
import datetime
from .models import InSubCategory, OutSubCategory
def grid(v1, v2) :
 
    RE = 6371.00877 # 지구 반경(km)
    GRID = 5.0      # 격자 간격(km)
    SLAT1 = 30.0    # 투영 위도1(degree)
    SLAT2 = 60.0    # 투영 위도2(degree)
    OLON = 126.0    # 기준점 경도(degree)
    OLAT = 38.0     # 기준점 위도(degree)
    XO = 43         # 기준점 X좌표(GRID)
    YO = 136        # 기1준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD
 
    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    rs = {}
    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = v2 * DEGRAD - olon
    if theta > math.pi :
        theta -= 2.0 * math.pi
    if theta < -math.pi :
        theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
    return rs

def exercise_recommendation(weather, index) : #운동 추천 함수
    in_cat = InSubCategory()
    out_cat = OutSubCategory()
    category = [] #운동 카테고리 저장. [0] = 실내 [1] = 야외
    category.append(in_cat.in_sub_categories) # weather[i].key != 0 
    in_recommendation = category[0][random.randrange(0,len(category[0]))][1]

    category.append(out_cat.out_sub_categories) # weather[i].key == 0 일때
    out_recommendation = category[1][random.randrange(0,len(category[1]))][1]
    if index+1 == 6 :
        if list(weather[index].values())[0] != '0':
            tmp_dict = list(weather[index].values())
            return in_recommendation
        else:
            return out_recommendation
    for i in range(index, index+2): # 1시간 뒤까지 판단.
        if list(weather[index].values())[0] != '0': #비소식이 있음.
            return in_recommendation
        
    return out_recommendation
        
def get_time(time_dict) : # 날씨 api에 넣을 시간데이터 함수
    now = datetime.datetime.now()
    not_now = now - datetime.timedelta(minutes=30) # 30분 전 시간을 데이터로 사용.
    time_dict['year'] = not_now.year
    time_dict['month'] = not_now.month
    time_dict['day'] = not_now.day
    time_dict['hour'] = not_now.hour
    time_dict['minute'] = not_now.minute

    
    if time_dict['month'] < 10: # 시간 데이터는 월/일/시/분이 모두 2자리를 차지해야해서 한 자리 수면 앞에 0을 붙여줌.
        time_dict['month'] = str(time_dict['month'])
        time_dict['month'] = '0' + time_dict['month']
    if time_dict['day'] < 10: 
        time_dict['day'] = str(time_dict['day'])
        time_dict['day'] = '0' + time_dict['day']
    if time_dict['hour'] < 10:
        time_dict['hour'] = str(time_dict['hour'])
        time_dict['hour'] = '0' + time_dict['hour']
    if time_dict['minute'] < 10:
        time_dict['minute'] = str(time_dict['minute'])
        time_dict['minute'] = '0' + time_dict['minute']
    

    return time_dict