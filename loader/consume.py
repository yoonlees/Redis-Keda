import json
import os
import time

from redis import Redis

REDIS_HOST = os.getenv('REDIS_SERVICE_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_SERVICE_PORT', '6379')

r = Redis(host=REDIS_HOST, port=int(REDIS_PORT))

if not r.llen('events'):
    print('no events to consume')
    exit(0)

event = json.loads(r.rpop('events').decode('utf-8'))

sleep = event['wait']
print(f'sleeping {sleep}s')
time.sleep(sleep)
print('(done)')
