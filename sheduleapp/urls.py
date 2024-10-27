from  django.urls import  path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import (add_judge, judge_full, two_site_judge, double_menu, home,
                    profile_view, register, judge_double_menu,
                    site_double_menu, two_site, add_site,login_view)


urlpatterns = [
path('add_judge/', add_judge, name='add_judge'),
path('add_site/', add_site, name='add_site'),
path('judge/', judge_full, name='judge_full'),
path('site_judge/<str:id>/', two_site_judge, name='two_site_judge'),
path('site/<str:id>/', two_site, name='two_site'),
path('double_menu/', double_menu, name='double_menu'),
path('judge_double_menu/', judge_double_menu, name='judge_double_menu'),
path('site_double_menu/', site_double_menu, name='site_double_menu'),
path('', home, name='home'),
path('profile/', profile_view, name='profile'),
path('register/', register, name='register'),
path('login/', login_view, name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')),
     name="logout"),
]