from django.urls import path
from . import views 

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<str:username>/", views.UserDetailView.as_view(), name="profile"),
    path("<str:chat_uuid>/", views.chat_view, name="chat"),
    path("start-chat/<str:username>/", views.get_or_create_chat, name="start-chat"),
]
