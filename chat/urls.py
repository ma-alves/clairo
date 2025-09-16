from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<int:pk>", views.UserDetailView.as_view(), name="profile"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.logout_view, name='logout')
]

# :3
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
