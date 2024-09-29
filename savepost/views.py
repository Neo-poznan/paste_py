import json
import subprocess
import logging
from datetime import datetime

import httpx
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from savepost.models import Posts
from savepost.yandex_s3 import upload_file_to_s3
from savepost.validators import date_validator

logger = logging.getLogger('django.request')



class NewPostView(View):
    template_name = 'savepost/index.html'

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
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get('http://127.0.0.1:8001/generate/')
                if response.status_code != 200:
                    raise httpx.HTTPError
                response_json = response.json()
        except httpx.HTTPError as e:
            logger.error(f'[{datetime.now()}] Ошибка при запросе к микросервису для генерации ключа! {e}')

        post_key = response_json['hash']       
        post_content = form_data['text']
        del_date = form_data['del_date']


        await date_validator(del_date)
        await upload_file_to_s3(post_content, post_key)
        await Posts.objects.acreate(key=post_key, del_date=del_date)
        # формируем ссылку на пост
        url = f'http://127.0.0.1:8000/p/{post_key}'

        return JsonResponse({'link': url})
    

def execute_code(request):
    '''
    Представление для выполнения кода в браузере
    '''
    # получаем данные из формы
    body_unicode = request.body.decode('utf-8')
    form_data = json.loads(body_unicode) 
    code = form_data['text']

    # удаляем лишние переносы строк
    code = code.strip()
    code_without_unnecessary_line_breaks = ''
    for line in code.split('\n'): 
        code_without_unnecessary_line_breaks += line.strip() + '\n' 

    # выполняем код
    executor = subprocess.run(
        ['python', '-c', code_without_unnecessary_line_breaks],
        capture_output=True,
        text=True
    )
    
    return JsonResponse({'stdout': executor.stdout, 'stderr': executor.stderr})



