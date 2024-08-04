import redis

from django.shortcuts import render
from django.contrib.sessions.models import Session

from getpost.yandex_s3 import download_file_from_s3
from savepost.models import PostUrls

def get_text_view(request, post_key):
    '''Если поста нет, то выводится соответствующее сообщение,
    если пост есть, то выводится текст поста взятый из кэша если он есть, 
    иначе получаем его из s3 и кэшируем на 30 минут'''
    redis_client = redis.StrictRedis(host='localhost', port=6379)
    # если поста нет в БД
    try:
        post = PostUrls.objects.get(key=post_key)
    except PostUrls.DoesNotExist:
        return render(request, 'getpost/post.html',
            context={'post_text': 'Поста, который вы ищите не существует или он был удален'})   
    # если данный пользователь еще не просматривал данный пост, то увеличиваем счетчик просмотров
    if not post_key in request.session:
        request.session[post_key] = True 
        post.views += 1
        post.save()

    # если текст пост есть в кэше
    if redis_client.exists(post_key):
        post_text = redis_client.get(post_key).decode('utf-8')
    # если текста поста нет в кэше
    else:  
        post_text = download_file_from_s3(post.file_url)
        # кэшируем пост
        redis_client.set(post_key, post_text)
        redis_client.expire(post_key, 1800)
    return render(request, 'getpost/post.html', context={'post_text': post_text, 'views': post.views})
    
