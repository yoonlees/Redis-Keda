import json
import os
import time
from random import Random

from redis import Redis

REDIS_HOST = os.getenv('REDIS_SERVICE_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_SERVICE_PORT', '6379')

r = Redis(host=REDIS_HOST, port=int(REDIS_PORT))

while True:
    print('publishing events:')
    for i in range(10):
        event = {'wait': Random().randint(10, 20)}
        r.lpush('events', json.dumps(event))
        print(f'- {event}')

    print('')
    print('sleeping for 10s')
    time.sleep(10)
    print('')
