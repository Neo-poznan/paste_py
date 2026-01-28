import base64
import hashlib
import logging
import celery
import redis
import psycopg2
from functools import lru_cache
from asgiref.sync import sync_to_async

from config import settings
from config.settings import PREPARED_URLS_COUNT, PREPARED_URLS_FILL_INTERVAL, REDIS_HOST, REDIS_PORT

logger = logging.getLogger('django.request')

app = celery.Celery('unique_url_generator', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')


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
    sender.add_periodic_task(PREPARED_URLS_FILL_INTERVAL, key_generation_task.s(), name='generate key')


@app.task
def key_generation_task():
    '''
    Celery task to generate unique keys and store them in Redis list
    '''
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    current_prepared_urls_count = redis_client.llen('prepared_urls')
    urls_to_generate = PREPARED_URLS_COUNT - current_prepared_urls_count
    if urls_to_generate <= 0:
        logger.info('No need to generate new keys. Current prepared keys count: %d', current_prepared_urls_count)
        return
    for _ in range(urls_to_generate):
        new_key = generate_unique_key()
        redis_client.rpush('prepared_urls', new_key)
    logger.info('Generated %d new keys. Total prepared keys count: %d', urls_to_generate, redis_client.llen('prepared_urls'))


def generate_unique_key() -> str:
    '''
    Generate a unique key for a post
    '''
    unique_number = get_unique_number()
    orig_id = str(unique_number).encode('utf-8')  
    hash_object = hashlib.sha256(orig_id)
    hash_digest = hash_object.digest()
    short_url_byte = base64.urlsafe_b64encode(hash_digest)[:13]   
    short_url = short_url_byte.decode('utf-8')
    return short_url


def get_unique_number() -> int:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT nextval('unique_key_sequence');")
        result = cursor.fetchone()
        return result[0]


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


async def get_hash() -> str:
    '''
    Get a unique key for a new post, either from prepared keys or by generating a new one
    '''

    redis_client = await redis.asyncio.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
    post_key = await redis_client.lpop('prepared_urls')
    if post_key is None:
        # If there are no prepared keys, generate a new one
        post_key = await sync_to_async(generate_unique_key)()
        logger.warning('No prepared keys available, generated a new key: %s', post_key)
    else:
        post_key = post_key.decode('utf-8')
    await redis_client.close()
    return post_key