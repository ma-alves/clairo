from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('search/', views.search_users, name='search'),
	path('profile/<str:username>/', views.UserDetailView.as_view(), name='profile'),
	path('start-chat/<str:username>/', views.get_or_create_chat, name='start-chat'),
	path('<uuid:chat_uuid>/', views.chat_view, name='chat'),
]
