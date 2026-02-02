import logging
import base64
import hashlib

from asgiref.sync import sync_to_async

import redis

logger = logging.getLogger('django.request')


def generate_unique_key(connection) -> str:
    '''
    Generate a unique key for a post
    '''
    unique_number = get_unique_number(connection)
    orig_id = str(unique_number).encode('utf-8')  
    hash_object = hashlib.sha256(orig_id)
    hash_digest = hash_object.digest()
    short_url_byte = base64.urlsafe_b64encode(hash_digest)[:13]   
    short_url = short_url_byte.decode('utf-8')
    return short_url


def get_unique_number(connection) -> int:
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('unique_key_sequence');")
        result = cursor.fetchone()
        return result[0]

async def get_key(connection, redis_host: str, redis_port: str) -> str:
    '''
    Get a unique key for a new post, either from prepared keys or by generating a new one
    '''

    redis_client = await redis.asyncio.from_url(f'redis://{redis_host}:{redis_port}/0')
    post_key = await redis_client.lpop('prepared_urls')
    if post_key is None:
        post_key = await sync_to_async(generate_unique_key)(connection=connection)
        logger.warning('No prepared keys available, generated a new key: %s', post_key)
    else:
        post_key = post_key.decode('utf-8')
    await redis_client.close()
    return post_key

