import logging
import celery
import redis

from config.settings import PREPARED_URLS_COUNT, PREPARED_URLS_FILL_INTERVAL, REDIS_HOST, REDIS_PORT

logger = logging.getLogger('django.request')

app = celery.Celery('unique_url_generator', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

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
    import string
    import random

    key_length = 8
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(key_length))

async def get_hash() -> str:
    '''
    Get a unique key for a new post, either from prepared keys or by generating a new one
    '''

    redis_client = await redis.asyncio.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
    post_key = await redis_client.lpop('prepared_urls')
    if post_key is None:
        # If there are no prepared keys, generate a new one
        post_key = generate_unique_key()
        logger.warning('No prepared keys available, generated a new key: %s', post_key)
    else:
        post_key = post_key.decode('utf-8')
    await redis_client.close()
    return post_key