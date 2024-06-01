from django.urls import path

from savepost import views

app_name = 'savepost'

urlpatterns = [
    path('', views.NewPostView.as_view(), name='new_post'),
    path('success/<path:url>/', views.success_view, name='success'),
]