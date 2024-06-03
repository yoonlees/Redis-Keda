import json
import os
import time

from redis import Redis

REDIS_HOST = os.getenv('REDIS_SERVICE_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_SERVICE_PORT', '6379')

r = Redis(host=REDIS_HOST, port=int(REDIS_PORT))

while r.llen('events'):
    event = json.loads(r.rpop('events').decode('utf-8'))

    sleep = event['wait']
    print(f'sleeping {sleep}s', end='')
    time.sleep(sleep)
    print(' (done)')
