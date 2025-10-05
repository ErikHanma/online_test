from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    
    # Тесты
    path('test/<int:pk>/', views.test_detail, name='test_detail'),
    path('test/<int:pk>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:pk>/result/<int:result_pk>/', views.test_result, name='test_result'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='test_list'), name='logout'),
    
    # Профиль
    path('profile/', views.profile, name='profile'),
]