from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/<int:pk>/', views.test_detail, name='test_detail'),
]