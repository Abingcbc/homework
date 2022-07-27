import logging
import random
import requests
import logging
import warnings
import time

count = 0
user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
]

def write_result(item):
    global count
    if not item['validation']:
        return
    count += 1
    log(item['ID'] + ' : ' + str(count))
    with open('found.txt', 'a') as file:
        file.write(item['ID']+'\n')
    with open('results.txt', 'a') as file:
        for key, value in item.items():
            if key == 'meta_info':
                for k, v in value.items():
                    if v.strip() == '':
                        continue
                    file.write(k.strip().replace(':','') + ': ' 
                    + v.strip().replace(':','') + '\n')
            elif key == 'validation':
                continue
            elif value.strip() == '':
                    continue
            else:
                file.write(key.strip().replace(':','') + ': ' 
                + value.strip().replace(':','') + '\n')
        file.write('\n')

# print log in console and into file
def log(message):
    # warnings.filterwarnings('ignore')

    # logging.basicConfig(
    #     level=logging.INFO,
    #     filename="amazon.log",
    #     filemode="a",
    #     format="%(asctime)s - %(levelname)s: %(message)s",
    # )
    print(message)
    # logging.info(message)

def new_request(request, spider):
    if request.meta.get('robot') == 1:
        print('robot check request ' + request.url + ' ' + request.meta['proxy'])
        return request
    request.headers['User-Agent'] = random.choice(user_agents)
    request.meta['proxy'] = 'http://' + get_proxy()
    # request.cookies = spider.cookieJar.extract_cookies()
    # print(request.cookies)
    log('Using proxy: ' + request.meta['proxy'])
    log(request.url)
    return request

def get_proxy():
    response = eval(requests.get('http://127.0.0.1:5010/get/').text).get('proxy')
    while response is None:
        print('----------')
        response = eval(requests.get('http://127.0.0.1:5010/get/').text).get('proxy')
        time.sleep(5)
    return response