from  django.urls import  path
from .views import show_base_sites


urlpatterns = [
path('sites/', show_base_sites, name='show_base_sites'),
]