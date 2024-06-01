from django.urls import path

from getpost import views

app_name = 'getpost'

url_patterns = [
    path('<str:hash>/', views.get_post_url, name='get_url'),
    path('get/', views.get_text, name='get_text')
]