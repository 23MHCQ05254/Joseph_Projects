from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', views.add_book, name='add_book'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('send-message/', views.send_message, name='send_message'),
    path('user-search/', views.user_search, name='user_search'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
]
