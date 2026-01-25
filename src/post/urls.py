from django.urls import path

from post import views

app_name = 'post'

urlpatterns = [
    path('', views.CreateNewPostView.as_view(), name='new_post'),
    path('execute_code/', views.execute_code_view, name='execute_code'),
    path('p/<str:post_key>/', views.get_post_view, name='get_post'),
]

