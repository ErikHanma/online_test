from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/<int:pk>/', views.test_detail, name='test_detail'),
    path('test/<int:pk>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:pk>/result/<int:result_pk>/', views.test_result, name='test_result'),
]