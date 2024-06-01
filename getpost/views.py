from django.shortcuts import render, redirect
from django.urls import reverse_lazy


def get_post_url(request, key):


    request.META['post_url'] = 0 # тут данные из бд
    return redirect(request, reverse_lazy('ссылка на получение поста'))

def get_text(request):
    pass


