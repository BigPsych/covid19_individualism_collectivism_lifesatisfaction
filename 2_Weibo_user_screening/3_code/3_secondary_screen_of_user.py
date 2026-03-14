import csv
import json
import time
import pytz
import requests
from datetime import datetime, timedelta
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "Referer": "https://weibo.com/ajax/statuses/buildComments?flow=1&is_reload=1&id=4878537754156845&is_show_bulletin=2&is_mix=0&count=10&uid=7690282045&fetch_level=0&locale=zh-CN",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
#字典格式
cookies = {'XSRF-TOKEN': 'gKnCBY5pVvvs0spVagSvmeVn', 'SCF': 'ArS8GOMcx4zM8khMHUIso8mxGNLQWbCKZmHgryBuGKv_kHORmetRAAeyBszPORl_A_cBb3yeaiM1n29Z7y85-mc.', '_s_tentry': 'weibo.com', 'Apache': '4958883643985.188.1724656970855', 'SINAGLOBAL': '4958883643985.188.1724656970855', 'ULV': '1724656970862:1:1:1:4958883643985.188.1724656970855:', 'UOR': ',,cn.bing.com', 'ALF': '1737185971', 'SUB': '_2A25KZ73jDeRhGeFG41sY8ijKzz6IHXVpHL8rrDV8PUJbkNB-LWr4kW1NeJ72mCKJyyKkGVXBBEnZK8w7_Cw6DzFy', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5F6ZQ2uvdf8JMmlVB0g_be5JpX5KMhUgL.FoMR1h.4eoqcShz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1hn41KzcSoBE', 'WBPSESS': 'ExkktpaA-4CRe1RiH-_VWt0gdfrfpC9l6QI6IXt0EoHL6cO2e4gPJQJISvPnnMHlij3pnKsw6xQGr-9FmyYVEnwS3j3vzt6uS_1u2w4B1CUyQK-YRC0Gp4DU0ci31LXeV7NlJbxzk4sNE2KAc9B1nQ=='}

def start():
    #筛选注册时间18年之前注册
    cd = csv.reader(open('用户.csv', 'r', encoding='utf-8'))
    for i in cd:
        time.sleep(1)
        uid = i[1]
        url = f'https://weibo.com/ajax/profile/detail?uid={uid}'
        print(url)
        try:
            respons = requests.get(url, headers=headers, cookies=cookies).json()
            created_at = respons['data']['created_at'].split('-')[0]
            if int(created_at) < 2019:
                with open('注册时间.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                    fi = csv.writer(fi)
                    fi.writerow(
                        i + [respons['data']['created_at']]
                    )
        except:
            pass

def get_url():
    # 博文数量>1000< 2500
    cd = csv.reader(open('注册时间.csv', 'r', encoding='utf-8'))
    for i in cd:
        uid = i[1]
        time.sleep(0.5)
        try:
            url = f'https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0'
            response = requests.get(url, headers=headers, cookies=cookies).json()
            total = response['data']['total']
            text_raw = response['data']['list'][0]['text_raw'].replace('\n', '').replace('\r', '')
            if total > 1000 and total < 2500:
                with open('user.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                    fi = csv.writer(fi)
                    fi.writerow(
                        i + [total, text_raw]
                    )
        except:
            pass

def fen_si():
    # 粉丝数量< 5000
    cd = csv.reader(open('注册时间.csv', 'r', encoding='utf-8'))
    for i in cd:
        uid = i[3]
        time.sleep(0.5)
        try:
            url = f'https://weibo.com/ajax/profile/info?uid={uid}'
            response = requests.get(url, headers=headers, cookies=cookies).json()
            followers_count = response['data']['user']['followers_count']
            v_plus = response['data']['user']['v_plus']
            svip = response['data']['user']['svip']
            if followers_count < 5000:
                # 非黄V 蓝V
                if v_plus == 0 and svip == 0:
                    with open('用户-1.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                        fi = csv.writer(fi)
                        fi.writerow(
                            [followers_count, uid] + i
                        )

        except:
                pass

def content(mid, uid):
        url = "https://weibo.com/ajax/statuses/buildComments"
        params = {
            "flow": "1",
            "is_reload": "1",
            "id": mid,
            "is_show_bulletin": "2",
            "is_mix": "0",
            "count": "10",
            "uid": uid,
            "fetch_level": "0",
            "locale": "zh-CN"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        if response.status_code == 200:
            result = json.loads(response.text)
            data_list = result['data']
            for tr in data_list:
                followers_count = tr['user']['followers_count']
                uid = tr['user']['id']
                statuses_count = tr['user']['statuses_count']
                profile_url = tr['user']['profile_url']
                link = f'https://weibo.com/ajax/profile/detail?uid={uid}'
                v_plus = tr['user']['v_plus']

                if followers_count < 5000:
                    if v_plus == 0:
                        with open('用户.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                            fi = csv.writer(fi)
                            fi.writerow(
                                [followers_count, uid, statuses_count, profile_url, link]
                            )


start()