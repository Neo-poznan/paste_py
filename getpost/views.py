import redis

from django.shortcuts import render
from asgiref.sync import sync_to_async

from getpost.yandex_s3 import download_file_from_s3
from savepost.models import PostUrls
from pastebin.settings import REDIS_HOST, REDIS_PORT

async def get_text_view(request, post_key):
    '''Если поста нет, то выводится соответствующее сообщение,
    если пост есть, то выводится текст поста взятый из кэша если он есть, 
    иначе получаем его из s3 и кэшируем на 30 минут'''
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    
    # если поста нет в БД
    try:
        post_db_row = await PostUrls.objects.aget(key=post_key)
    except PostUrls.DoesNotExist:
        return render(request, 'getpost/post.html',
            context={'post_text': 'Поста, который вы ищите не существует или он был удален'})   
    # если данный пользователь еще не просматривал данный пост, то увеличиваем счетчик просмотров
    is_viewed = await sync_to_async(request.session.get)(post_key)
    if not is_viewed:
        await sync_to_async(request.session.__setitem__)(post_key, True)
        post_db_row.views += 1
    # обновляем последнюю дату вызова
    await post_db_row.asave()
    if redis_client.exists(post_key):
        post_content = redis_client.get(post_key).decode('utf-8')
    else:  
        post_content = await download_file_from_s3(post_db_row.file_url)
        # кэшируем пост
        redis_client.set(post_key, post_content)
        redis_client.expire(post_key, 1800)
    return render(request, 'getpost/post.html', context={'post_text': post_content, 'views': post_db_row.views})
    
