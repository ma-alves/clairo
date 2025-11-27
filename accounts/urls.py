from django.urls import path

from . import views

urlpatterns = [
	path('signup/', views.signup_view, name='signup'),
	path('token/', views.token, name='token'),
    path('reset-password/', views.token_reset_view, name='reset_password'),
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
