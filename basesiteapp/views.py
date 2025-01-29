""" 
Метод выводит для зарегистрированных пользователей на экран все сайты из БД - BaseSites
"""


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import BaseSites


@login_required
def show_base_sites(request):
    base_sites = BaseSites.objects.all()
    
    return render(request, "basesiteapp/showbasesites.html", {"sites":base_sites})
