import requests
from threading import Thread
from utils import *
import random
from init import start_urls, user_agents
from bs4 import BeautifulSoup
import re
import prime_parser
import ordinary_parser
import threading
import urllib
from imageRecognize.imageRec import parse_robot


def get_and_parse(url, item, session, thread_name):
    recieved = False
    # appKey = "Um1lYWlLRTBMbkVLWlN5NTphUzZHY0VGanVOc1RjSzJv"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "user-agent": random.choice(user_agents),
        # "Proxy-Authorization": 'Basic '+ appKey
    }
    # ip_port = 'secondtransfer.moguproxy.com:9001'
    # ip_port = requests.get('http://127.0.0.1:5000/get').text
    # ip_port = eval(ip_port)['proxies']
    # proxies = {"http": "http://" + ip_port}
    try:
        # session.proxies.update(proxies)
        response = session.get(url=url, headers=headers,
        timeout=20, verify=False, allow_redirects=True)
    except Exception as e:
        log(item["ID"] + ": " + str(e))
        # requests.get('http://127.0.0.1:5000/delete?proxy='+ip_port)
        start_urls.put(url)
        return -1
    response_code = response.status_code
    if response_code != 200:
        if response_code == 404:
            with open("not_found.log", "a") as file:
                file.write(item["ID"] + "\n")
                return 0
        log("ErrorCode: " + str(response_code))
        # requests.get('http://127.0.0.1:5000/delete?proxy='+ip_port)
        start_urls.put(url)
        return -1
    else:
        content = BeautifulSoup(response.text, "lxml")
        if not (content.find(name="title", text=re.compile("Robot Check")) is None):
            log("Robot check triggered " + url)
            pic = session.get(content.find(name='div', attrs={'class':'a-row a-text-center'}).
            find(name='img',attrs={'src':True})['src'])
            with open(thread_name+'.jpg','wb') as file:
                file.write(pic.content)
            capt_string = parse_robot(thread_name+'.jpg', thread_name)
            if capt_string == 'error':
                start_urls.put(url)
                return -1
            data = {
                'amzn':content.find(attrs={'name':'amzn'})['value'],
                'amzn-r':content.find(attrs={'name':'amzn-r'})['value'],
                'field-keywords': capt_string
            }
            r = session.get('https://www.amazon.com/errors/validateCapcha', 
            params=data,headers=headers,allow_redirects=True)
            with open('/Users/cbc/Desktop/1.html') as file:
                file.write(r.text)
            print(r.status_code)
            return get_and_parse(url, item, session, thread_name)
            # start_urls.put(url)
            # requests.get('http://127.0.0.1:5000/delete?proxy='+ip_port)
            # return -1
        else:
            page_type = content.find(id="productTitle")
            if page_type is None:
                # log("-" * 10 + item["ID"] + ": Prime" + "-" * 10)
                item["name"], item["star_score"], item["imdb_score"], item[
                    "time_len"
                ], item["year"], item["restrict_level"], item["rent_price"], item[
                    "buy_price"
                ], item[
                    "meta_info"
                ], item[
                    "validation"
                ] = prime_parser.prime_parse(
                    content, item["ID"]
                )
                recieved = True
            else:
                # log("-" * 10 + item["ID"] + ": Ordinary" + "-" * 10)
                item["name"], item["star_score"], item["imdb_score"], item[
                    "time_len"
                ], item["year"], item["restrict_level"], item["rent_price"], item[
                    "buy_price"
                ], item[
                    "meta_info"
                ], item[
                    "validation"
                ] = ordinary_parser.ordinary_parse(
                    content, item["ID"]
                )
                recieved = True
    if recieved:
        write_result(item)
        return 0
    return -1

def run(thread_name):
    while not start_urls.empty():
        session = requests.Session()
        url = start_urls.get()
        item = {}
        item["ID"] = url.split("/")[-1].strip()
        if get_and_parse(url, item, session, thread_name) < 0:
            print('Clear cookies')
            session.cookies.clear()


def crawl():
    threads = []

    for i in range(1):
        threads.append(threading.Thread(target=run, args=[str(i)]))

    for i in range(len(threads)):
        threads[i].start()
