from django.urls import path

from getpost import views


app_name = 'getpost'


urlpatterns = [
    path('<str:post_key>/', views.get_post_view, name='getpost'),
]

