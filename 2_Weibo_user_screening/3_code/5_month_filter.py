import csv
import time
import json
import requests
import calendar
from datetime import datetime
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
cookies = {'XSRF-TOKEN': 'gKnCBY5pVvvs0spVagSvmeVn', 'SCF': 'ArS8GOMcx4zM8khMHUIso8mxGNLQWbCKZmHgryBuGKv_kHORmetRAAeyBszPORl_A_cBb3yeaiM1n29Z7y85-mc.', '_s_tentry': 'weibo.com', 'Apache': '4958883643985.188.1724656970855', 'SINAGLOBAL': '4958883643985.188.1724656970855', 'ULV': '1724656970862:1:1:1:4958883643985.188.1724656970855:', 'UOR': ',,cn.bing.com', 'ALF': '1737185971', 'SUB': '_2A25KZ73jDeRhGeFG41sY8ijKzz6IHXVpHL8rrDV8PUJbkNB-LWr4kW1NeJ72mCKJyyKkGVXBBEnZK8w7_Cw6DzFy', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5F6ZQ2uvdf8JMmlVB0g_be5JpX5KMhUgL.FoMR1h.4eoqcShz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1hn41KzcSoBE', 'WBPSESS': 'ExkktpaA-4CRe1RiH-_VWt0gdfrfpC9l6QI6IXt0EoHL6cO2e4gPJQJISvPnnMHlij3pnKsw6xQGr-9FmyYVEnwS3j3vzt6uS_1u2w4B1CUyQK-YRC0Gp4DU0ci31LXeV7NlJbxzk4sNE2KAc9B1nQ=='
   }


def start():
    cd = csv.reader(open('用户.csv', 'r', encoding='utf-8'))
    for i in cd:
        time.sleep(1)
        url = i[-1]
        print(url)

        try:
            respons = requests.get(url, headers=headers, cookies=cookies).json()
            created_at = respons['data']['created_at'].split('-')[0]
            if int(created_at) < 2019:
                with open('用户-1.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                    fi = csv.writer(fi)
                    fi.writerow(
                        i + [respons['data']['created_at']]
                    )
        except:
            pass

def get_url():
    cd = csv.reader(open('用户.csv', 'r', encoding='utf-8'))
    for i in cd:
        uid = i[1]
        time.sleep(1)
        try:
            url = f'https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0'
            response = requests.get(url, headers=headers, cookies=cookies).json()
            total = response['data']['total']
            text_raw = response['data']['list'][0]['text_raw'].replace('\n', '').replace('\r', '')
            if total > 300:
                with open('user.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                    fi = csv.writer(fi)
                    fi.writerow(
                        i + [total, text_raw]
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

def host():
    for num in range(3, 1000):
        print(num)
        url = f"https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=102803&containerid=102803&extparam=discover%7Cnew_feed&max_id={num}&count=10"
        response = requests.get(url, headers=headers, cookies=cookies).json()
        statuses = response['statuses']
        for statuse in statuses:
            time.sleep(1)
            reposts_count = statuse['reposts_count']
            if reposts_count > 1:
                wb_text_raw = statuse['text_raw'].replace('\n', '')
                mid = statuse['mid']
                uid = statuse['user']['id']
                web_url = f'https://weibo.com/{mid}/{uid}'
                content(mid, uid)

def generate_month_dates(start_year, end_year):
    result = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # 获取每个月的第一天
            first_day = datetime(year, month, 1)
            # 获取每个月的最后一天
            last_day = datetime(year, month, calendar.monthrange(year, month)[1])
            # 转换为时间戳
            first_day_timestamp = int(first_day.timestamp())
            last_day_timestamp = int(last_day.timestamp())
            # 添加到结果列表
            result.append({
                "year": year,
                "month": month,
                "first_day": first_day,
                "last_day": last_day,
                "first_day_timestamp": first_day_timestamp,
                "last_day_timestamp": last_day_timestamp
            })
    return result

def user_sx(uid):
    dates = generate_month_dates(2019, 2023)
    # 输出结果
    for entry in dates:
        first_day_timestamp = f"{entry['first_day_timestamp']}"
        last_day_timestamp = f"{entry['last_day_timestamp']}"
        url = f'https://weibo.com/ajax/statuses/searchProfile?uid={uid}&page=1&starttime={first_day_timestamp}&endtime={last_day_timestamp}&hasori=1&hastext=1&haspic=1&hasvideo=1&hasmusic=1'
        try:
            respons = requests.get(url, headers=headers, cookies=cookies).json()
        except:
            respons = requests.get(url, headers=headers, cookies=cookies).json()
        trs = respons['data']['list']
        if trs == []:
           return False
    return True


# 博文
def bw():
    cd = csv.reader(open('符合用户.csv', 'r', encoding='utf-8'))
    for i in cd:
        time.sleep(1)
        uid = i[1]
        code = user_sx(uid)
        if code:
            with open('19-23年符合用户.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                fi = csv.writer(fi)
                fi.writerow(
                    i
                )

bw()