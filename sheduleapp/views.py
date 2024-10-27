from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Judges, Site, Profile
from .forms import (JudgeFrom, UserRegistrationForm, JudgeMenu, SiteMenu,
                    SiteFrom)
from datetime import date
from django.contrib import messages

@login_required
def add_judge(request):
    if request.method == 'POST':
        form = JudgeFrom(request.POST)
        message = 'Ошибка в заполнение данных'
        if form.is_valid():
            arbitration_court = form.cleaned_data["arbitration_court"]
            name = form.cleaned_data["name"]
            cabinet = form.cleaned_data["cabinet"]
            day_name = form.cleaned_data["day_name"]
            if arbitration_court == "АС СПб":
                url = f'https://schedule.arbitr.ru/Schedule/Operator/?courtTag=SPB&cabinetName={cabinet}'
            else:
                url = (f'https://schedule.arbitr.ru/Schedule/Operator'
                       f'/?courtTag=13AAS&cabinetName={cabinet}')
            judge = Judges(arbitration_court= arbitration_court, name=name,
                        cabinet=cabinet, day_name=day_name, url=url)
            judge.save()
            messages.success(request, 'Судья успешно добавлен!')
            return redirect('add_judge')  # Переадресация на ту же страницу
    else:
        form = JudgeFrom() # Если GET запрос, то возврат данных
        message = "Заполните поля судьи"

    return render(request, 'sheduleapp/judge_form.html', {'form':form,
                                                        "message": message})

@login_required
def add_site(request):
    if request.method == 'POST':
        form = SiteFrom(request.POST)
        message = 'Ошибка в заполнение данных'
        if form.is_valid():
            title = form.cleaned_data["title"]
            url = form.cleaned_data["url"]
            site = Site(title= title, url=url)
            site.save()
            messages.success(request, 'Сайт успешно добавлен!')
            return redirect('add_site')  # Переадресация на ту же страницу
    else:
        form = SiteFrom() # Если GET запрос, то возврат данных
        message = "Заполните поля сайта"

    return render(request, 'sheduleapp/site_form.html', {'form':form,
                                                        "message": message})



@login_required
# def judge_full(request, post_id)
def judge_full(request):
    today = date.today()
    dict_day = {0:"ПН", 1:"ВТ", 2:"СР", 3:"ЧТ", 4:"ПТ"}
    judges = Judges.objects.filter(day_name=dict_day.get(today.weekday()))
    context = {"judges": judges,
               'today': today}
    return render(request, 'sheduleapp/shedule_new_day.html', context)

@login_required
def two_site_judge(request, id):
    list_id = id.split('&')
    list_id=list(int(x) for x in list_id)
    sites = Judges.objects.filter(pk__in=list_id)
    context = {'sites': sites}
    return render(request, 'sheduleapp/two_site.html', context)

@login_required
def two_site(request, id):
    list_id = id.split('&')
    list_id=list(int(x) for x in list_id)
    sites = Site.objects.filter(pk__in=list_id)
    context = {'sites': sites}
    return render(request, 'sheduleapp/two_site.html', context)

@login_required
def double_menu(request):
    return render(request, 'sheduleapp/double_menu.html')


def home(request):
    return render(request, 'sheduleapp/home.html')


@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    return render(request, 'sheduleapp/profile.html', {'profile':profile,
                                                       'user':user})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # перенаправляем на главную страницу
        else:
            messages.error(request,"Нет такого пользователя. Пройдите регистрацию.")
            return redirect('login')  # возвращаем обратно на страницу входа
    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.set_password(user.cleaned_data['password'])
            user.save()
            birth_date = form.cleaned_data['birth_date']
            bio =  form.cleaned_data['bio']
            profile = Profile.objects.create(user=user, birthday=birth_date,
                                             bio=bio)
            profile.save()
            return redirect('login')  # Перенаправление пользователю на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': form})

@login_required
def judge_double_menu(request):
    if request.method == 'POST':
        message = ""
        form = JudgeMenu(request.POST)
        if form.is_valid():
            selected_choices = form.cleaned_data['choices']
            if len(selected_choices) >2:
                message = "Пожалуйста, выберите ровно два варианта."
            else:
                # Преобразуем объекты в список идентификаторов
                selected_ids = [choice.id for choice in selected_choices]
                # Формируем строку параметров для передачи на другой сайт
                params = '&'.join(f'{id}' for id in selected_ids)
                # Переходим на новый сайт с параметрами
                return redirect('two_site_judge', id=params)
    else:
        form = JudgeMenu()
        message = ""
    return render(request, 'sheduleapp/double_menu_judge.html', {'form':form,
                                                        "message": message})
@login_required
def site_double_menu(request):
    if request.method == 'POST':
        message = ""
        form = SiteMenu(request.POST)
        if form.is_valid():
            selected_choices = form.cleaned_data['choices']
            if len(selected_choices) >2:
                message = "Пожалуйста, выберите ровно два варианта."
            else:
                # Преобразуем объекты в список идентификаторов
                selected_ids = [choice.id for choice in selected_choices]
                # Формируем строку параметров для передачи на другой сайт
                params = '&'.join(f'{id}' for id in selected_ids)
                # Переходим на новый сайт с параметрами
                return redirect('two_site', id=params)
    else:
        form = SiteMenu()
        message = ""
    return render(request, 'sheduleapp/double_menu_site.html', {'form':form,
                                                        "message": message})