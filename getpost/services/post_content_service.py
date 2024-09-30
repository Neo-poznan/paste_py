import redis

from pastebin.settings import REDIS_HOST, REDIS_PORT

from getpost.yandex_s3 import download_file_from_s3

async def get_and_cache_post_content(post_key):
    '''Если текст поста есть в кэше то возвращает его, а если нет,
     то загружает его и кэширует'''
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    if redis_client.exists(post_key):
        post_content = redis_client.get(post_key).decode('utf-8')
    else:  
        post_content = await download_file_from_s3(post_key)
        # кэшируем пост
        if post_content != 'Ошибка загрузки контента!':
            redis_client.set(post_key, post_content)
            redis_client.expire(post_key, 1800)
    return post_content

    