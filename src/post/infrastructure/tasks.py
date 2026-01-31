import logging
from functools import lru_cache

import celery
import redis
import psycopg2

from ...config import settings
from .url_generator import generate_unique_key

logger = logging.getLogger('django.request')

app = celery.Celery('unique_url_generator', broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')


def create_sequence_if_not_exists():
    '''
    Create a sequence in the database if it does not exist
    '''
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            '''
            CREATE SEQUENCE IF NOT EXISTS unique_key_sequence START WITH 1 INCREMENT BY 1;
            '''
        )


@app.on_after_configure.connect
def setup_periodic_tasks(sender: celery.Celery, **kwargs):
    sender.add_periodic_task(settings.PREPARED_URLS_FILL_INTERVAL, key_generation_task.s(), name='generate key')


@app.task
def key_generation_task():
    '''
    Celery task to generate unique keys and store them in Redis list
    '''
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    current_prepared_urls_count = redis_client.llen('prepared_urls')
    urls_to_generate = settings.PREPARED_URLS_COUNT - current_prepared_urls_count
    if urls_to_generate <= 0:
        logger.info('No need to generate new keys. Current prepared keys count: %d', current_prepared_urls_count)
        return
    create_sequence_if_not_exists()
    for _ in range(urls_to_generate):
        new_key = generate_unique_key(connection=get_connection())
        redis_client.rpush('prepared_urls', new_key)
    logger.info('Generated %d new keys. Total prepared keys count: %d', urls_to_generate, redis_client.llen('prepared_urls'))


@lru_cache(maxsize=1)
def get_connection():
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )
    return conn

