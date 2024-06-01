import requests
import json

from django.contrib.sites.models import Site
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from savepost.models import PostUrls
from savepost.yandex_s3 import upload_file_to_s3


class NewPostView(View):
    template_name = 'savepost/index.html'

    def get(self, request):  
        return render(self.request, self.template_name)
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        form_data = json.loads(body_unicode)

        # тут будет функционал для запроса к микросервису для получения ключа
        key = 'mKOrf35OigM-e' # пока буду просто вписывать сюда тестовые ключи

        text = form_data['text']
        date = form_data['del_date']
        #$file_url = upload_file_to_s3(text, key)
        #PostUrls.objects.create(key=key, file_url=file_url, del_date=date)
        current_site = Site.objects.get_current()
        
        url = f'https://{current_site.domain}/{key}'


        return JsonResponse({'link': url})
    

def success_view(request, url):
    return render(request, 'savepost/success.html', context={'url': url})
    
