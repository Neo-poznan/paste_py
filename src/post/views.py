import json

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from post.models import Posts
from config.settings import SERVER_URL
from post.services.s3 import upload_file_to_s3
from post.validators import post_date_validator
from post.services.get_url_service import get_hash
from post.services.code_execute_service import execute_code
from asgiref.sync import sync_to_async
from post.services.post_content_service import get_and_cache_post_content, remove_unnecessary_line_breaks


class CreateNewPostView(View):
    template_name = 'post/index.html'
    

    async def get(self, request):  
        'Когда нужно просто отобразить страницу'
        return render(self.request, self.template_name)
    

    async def post(self, request):
        '''Когда пользователь отправляет форму принимаем ее в формате json
        запрашиваем ключ для нее, сохраняем в БД данные для удаления и просмотров,
         и сохраняем текст в хранилище s3 потом отправляем ссылку обратно пользователю'''
        body_unicode = request.body.decode('utf-8')
        form_data = json.loads(body_unicode)
        # запрос к микросервису для получения ключа
        post_key = await get_hash()
        post_content = form_data['text']
        del_date = form_data['del_date']
        post_date_validator(del_date)
        post_content = remove_unnecessary_line_breaks(post_content)
        post_filename = post_key + '.txt'
        await upload_file_to_s3(post_content, post_filename)
        await Posts.objects.acreate(key=post_key, delete_date=del_date)
        # формируем ссылку на пост
        url = f'{SERVER_URL}/p/{post_key}'

        return JsonResponse({'link': url})
    

async def execute_code_view(request):
    '''
    Представление для выполнения кода в браузере
    '''
    body_unicode = request.body.decode('utf-8')
    form_data = json.loads(body_unicode) 
    code = form_data['text']
    code = remove_unnecessary_line_breaks(code)
    result = await execute_code(code)
    return JsonResponse(result)


async def get_post_view(request, post_key):
    '''Если поста нет, то выводится соответствующее сообщение,
    если пост есть, то выводится текст поста и обновляется счетчик просмотров'''
    # если поста нет в БД
    try:
        post_metadata = await Posts.objects.aget(key=post_key)
    except Posts.DoesNotExist:
        return render(request, 'post/post.html',
            context={'post_text': 'Поста, который вы ищите не существует или он был удален'})   
    # если данный пользователь еще не просматривал данный пост, то увеличиваем счетчик просмотров
    is_viewed = await sync_to_async(request.session.get)(post_key)
    if not is_viewed:
        await sync_to_async(request.session.__setitem__)(post_key, True)
        post_metadata.views_count += 1
    # обновляем последнюю дату вызова
    await post_metadata.asave()
    # получаем текст поста
    post_content = await get_and_cache_post_content(post_key)
    return render(request, 'post/post.html', context={'post_text': post_content, 'views': post_metadata.views_count})

