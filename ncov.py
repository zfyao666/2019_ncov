import requests
import json
import mysql.connector as mc
import time
from requests.exceptions import RequestException


def get_response(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content.decode()
        return None
    except RequestException:
        print('WRONG!!!')
        return None


def get_all_data(url, headers):
    all_data = json.loads(json.loads(get_response(url, headers)).get('data')).get('areaTree')
    return all_data


def get_each_country_data(url, headers):
    all_data = get_all_data(url, headers)
    country, confirm, suspect, heal, dead, dead_rate, heal_rate = list(), list(), list(), list(), list(), list(), list()
    for data in all_data:
        country.append(data.get('name'))
        confirm.append(data.get('total')['confirm'])
        suspect.append(data.get('total')['suspect'])
        heal.append(data.get('total')['heal'])
        dead.append(data.get('total')['dead'])
        dead_rate.append(data.get('total')['deadRate'])
        heal_rate.append(data.get('total')['healRate'])
    return list(zip(country, confirm, suspect, heal, dead, dead_rate, heal_rate))


def get_each_province_data(url, headers):
    province_data = get_all_data(url, headers)[0].get('children')
    proince, confirm, suspect, heal, dead, dead_rate, heal_rate = list(), list(), list(), list(), list(), list(), list()
    for data in province_data:
        proince.append(data.get('name'))
        confirm.append(data.get('total')['confirm'])
        suspect.append(data.get('total')['suspect'])
        heal.append(data.get('total')['heal'])
        dead.append(data.get('total')['dead'])
        dead_rate.append(data.get('total')['deadRate'])
        heal_rate.append(data.get('total')['healRate'])
    return list(zip(proince, confirm, suspect, dead, heal, heal_rate, dead_rate))


def write_to_country(url, headers):
    print('>>>>>各国数据录入中>>>>>')
    conn = mc.connect(host='localhost', user='root', password='root', database='2019_nCov')
    mycursor = conn.cursor()
    sql = 'REPLACE INTO country (name, total_confirm, total_suspect, ' \
          'total_heal, total_dead, dead_rate, heal_rate) VALUES (' \
          '%s, %s, %s, %s, %s, %s, %s)'
    val = get_each_country_data(url, headers)
    mycursor.executemany(sql, val)
    conn.commit()
    mycursor.close()
    conn.close()
    print('>>>>>各国数据录入完毕>>>>>')


def write_to_province(url, headers):
    print('>>>>>各市数据录入中>>>>>')
    conn = mc.connect(host='localhost', user='root', password='root', database='2019_nCov')
    mycursor = conn.cursor()
    sql = 'REPLACE INTO province (name, confirm, suspect, dead, heal, healRate, deadRate)' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    val = get_each_province_data(url, headers)
    mycursor.executemany(sql, val)
    conn.commit()
    mycursor.close()
    conn.close()
    print('>>>>>各地区录入完毕>>>>>')



def main():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.100 Safari/537.36'}
    write_to_country(url, headers)
    time.sleep(6)
    write_to_province(url, headers)
