from django.shortcuts import render
from django.contrib.sessions.models import Session


from getpost.yandex_s3 import download_file_from_s3
from savepost.models import PostUrls


def get_text_view(request, post_key):
    # если поста нет в БД
    try:
        post = PostUrls.objects.get(key=post_key)
    except PostUrls.DoesNotExist:
        return render(request, 'getpost/post.html',
            context={'post_text': 'Поста, который вы ищите не существует или он был удален'})

    session = request.session
    # если данный пользователь еще не просматривал данный пост, то увеличиваем счетчик просмотров
    if not post_key in request.session:
        request.session[post_key] = True 
        post.views += 1
        post.save()
    
    post_text = download_file_from_s3(post.file_url)
    return render(request, 'getpost/post.html', context={'post_text': post_text, 'views': post.views})
    

