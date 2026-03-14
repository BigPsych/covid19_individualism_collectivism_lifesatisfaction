import csv
import time
import json
import requests
import pandas as pd
import calendar
import datetime
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
cookies = {}


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

def get_quarters(start_year, end_year):
    quarters = []
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            if quarter == 1:
                start_date = datetime.date(year, 1, 1)
                end_date = datetime.date(year, 3, 31)
            elif quarter == 2:
                start_date = datetime.date(year, 4, 1)
                end_date = datetime.date(year, 6, 30)
            elif quarter == 3:
                start_date = datetime.date(year, 7, 1)
                end_date = datetime.date(year, 9, 30)
            elif quarter == 4:
                start_date = datetime.date(year, 10, 1)
                end_date = datetime.date(year, 12, 31)
            quarters.append((start_date, end_date))
    return quarters

def date_to_timestamp(date):
    return int(time.mktime(date.timetuple()))

def user_sx(uid):
    start_year = 2019
    end_year = 2023
    quarters = get_quarters(start_year, end_year)
    for start_date, end_date in quarters:
        start_ts = date_to_timestamp(start_date)
        end_ts = date_to_timestamp(end_date)
        url = f'https://weibo.com/ajax/statuses/searchProfile?uid={uid}&page=1&starttime={start_ts}&endtime={end_ts}&hasori=1&hastext=1&haspic=1'
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
    # cd = csv.reader(open('符合用户.csv', 'r', encoding='utf-8'))
    # for i in cd:
    df = pd.read_excel('已筛选的活跃用户.xlsx')
    for i in df.values:
        uid = i[1]
        time.sleep(1)
        code = user_sx(uid)
        if code:
            with open('19-23年符合用户.csv', 'a+', encoding='utf-8-sig', newline='') as fi:
                fi = csv.writer(fi)
                fi.writerow(
                    i
                )

bw()