import json
import requests
import logging
from datetime import datetime

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from savepost.models import PostUrls
from savepost.yandex_s3 import upload_file_to_s3

logger = logging.getLogger('django.request')

class NewPostView(View):
    template_name = 'savepost/index.html'

    def get(self, request):  
        'Когда нужно просто отобразить страницу'
        return render(self.request, self.template_name)
    
    def post(self, request):
        '''Когда пользователь отправляет форму принимаем ее в формате json
        запрашиваем ключ для нее, сохраняем в БД данные для удаления и просмотров,
         и сохраняем текст в хранилище s3 потом отправляем ссылку обратно пользователю'''
        body_unicode = request.body.decode('utf-8')
        form_data = json.loads(body_unicode)

        # запрос к микросервису для получения ключа
        try:
            response = requests.get('http://127.0.0.1:8001/generate').json()
        except Exception as e:
            logger.error(f'[{datetime.now()}] Ошибка при запросе к микросервису для генерации ключа! {e}')
        key = response['hash']
        print(key)
        
        text = form_data['text']
        date = form_data['del_date']

        file_url = upload_file_to_s3(text, key)
        PostUrls.objects.create(key=key, file_url=file_url, del_date=date)
        # формируем ссылку на пост
        url = f'http://127.0.0.1:8000/p/{key}'

        return JsonResponse({'link': url})

