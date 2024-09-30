from django.shortcuts import render
from asgiref.sync import sync_to_async

from getpost.services.post_content_service import get_and_cache_post_content
from savepost.models import Posts


async def get_post_view(request, post_key):
    '''Если поста нет, то выводится соответствующее сообщение,
    если пост есть, то выводится текст поста и обновляется счетчик просмотров'''
    # если поста нет в БД
    try:
        post_db_row = await Posts.objects.aget(key=post_key)
    except Posts.DoesNotExist:
        return render(request, 'getpost/post.html',
            context={'post_text': 'Поста, который вы ищите не существует или он был удален'})   
    # если данный пользователь еще не просматривал данный пост, то увеличиваем счетчик просмотров
    is_viewed = await sync_to_async(request.session.get)(post_key)
    if not is_viewed:
        await sync_to_async(request.session.__setitem__)(post_key, True)
        post_db_row.views += 1
    # обновляем последнюю дату вызова
    await post_db_row.asave()
    # получаем текст поста
    post_content = await get_and_cache_post_content(post_key)
    return render(request, 'getpost/post.html', context={'post_text': post_content, 'views': post_db_row.views})
    
