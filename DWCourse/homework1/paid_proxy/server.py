from flask import Flask
import redis
from flask_apscheduler import APScheduler
import requests
from flask import g
import random
import json
from flask import request


app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost', port=6379, db=1, password='friday')


@app.route('/get')
def get():
    db = redis.Redis(connection_pool=pool)
    length = db.llen('proxies')
    proxy = str(db.lindex('proxies', random.randint(0, length))).replace("b'",'')
    return json.dumps({'proxies': str(proxy).replace("'",'')})

@app.route('/delete/')
def delete():
    db = redis.Redis(connection_pool=pool)
    proxy = request.args.get("proxy")
    db.lrem('proxies',0,proxy)
    return json.dumps({})

@app.route('/valid')
def valid():
    db = redis.Redis(connection_pool=pool)
    if db.llen('proxies') == 0:
        return json.dumps({'valid': 0})
    else:
        return json.dumps({'valid': 1})

def get_proxies():
    url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=e35c172757204768932db17bb209ed97&count=5&expiryDate=0&format=1&newLine=2'
    response = requests.get(url)
    if response.status_code == 200 and eval(response.text)['code'] == '0':
        db = redis.Redis(connection_pool=pool)
        msg = eval(response.text)['msg']
        print(msg)
        for p in msg:
            db.rpush('proxies', p['ip']+':'+p['port'])

class Config(object):
    JOBS = [
        {
            'id':'gp',
            'func':'server:get_proxies',
            'trigger':'interval',
            'seconds':10
        }
    ]
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run()