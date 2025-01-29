from  django.urls import  path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import (register, login_view,profile_view, CustomPasswordResetView)


urlpatterns = [
     path('register/', register, name='register'),
     path('login/', login_view, name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')),name="logout"),
     path('profile/', profile_view, name='profile_view'),
    path('password_reset/',CustomPasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name='password_reset',),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
