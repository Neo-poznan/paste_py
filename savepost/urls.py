from django.urls import path

from savepost import views

app_name = 'savepost'

urlpatterns = [
    path('', views.CreateNewPostView.as_view(), name='new_post'),
    path('execute_code/', views.execute_code_view, name='execute_code'),
]

