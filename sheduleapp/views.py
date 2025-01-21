from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import urllib.parse

from .models import Judges, Site, Profile
from .forms import (JudgeFrom, UserRegistrationForm, JudgeMenu, SiteMenu,
                    SiteFrom)

# открытие основной странице для входа или регистрации
def home(request):
    return render(request, 'sheduleapp/home.html')


# вход (аутентификация)
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

# регистрация пользователя

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            if user is not None:  # Проверяем, что аутентификация прошла успешно
                login(request, user)  # Входим в систему
                mail_subject = 'Регистрация на сайте - успешна!'  # Заголовок письма
                message = (f"Привет, {form.cleaned_data['first_name']}!\n"
                            f"Благодарим за регистрацию на сайте.\n"
                            f"Ваши данные:\n"
                            f"- почта {form.cleaned_data['email']},\n"
                            f"- пароль {form.cleaned_data.get('password1')}")
                to_email = form.cleaned_data.get('email')  # Получатель письма
                
                try:
                    send_mail(
                        subject=mail_subject,  # Заголовок письма
                        message=message,  # Сообщение
                        from_email=settings.EMAIL_HOST_USER,  # От кого отправляется письмо
                        recipient_list=[to_email],  # Список получателей
                        fail_silently=False  # Показывать исключения
                    )
                    
                    messages.success(request, f'Письмо успешно отправлено на {to_email}.')
                    logger.info(f'Письмо успешно отправлено на {to_email}.')
                except Exception as e:
                    messages.error(request, f'Не удалось отправить письмо: {e}')
                    logger.error(f'Не удалось отправить письмо: {e}')
                
                return redirect('home')
            else:
                # Обработка случая, когда аутентификация не удалась
                form.add_error(None, 'Ошибка аутентификации. Пожалуйста, проверьте введенные данные.')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
  

# открытие профиля пользователя после входа
@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    return render(request, 'sheduleapp/profile.html', {'profile':profile,
                                                       'user':user})

# Добавление судьи в БД
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

            # Добавление URL страницы расписания
            if arbitration_court == "АС СПб":
                url = f'https://schedule.arbitr.ru/Schedule/Operator/?courtTag=SPB&cabinetName={cabinet}'
            else:
                url = (f'https://schedule.arbitr.ru/Schedule/Operator'
                       f'/?courtTag=13AAS&cabinetName={cabinet}')

            # привязка судьи к конкретному пользователю

            judge = Judges.objects.create(user=request.user,
                           arbitration_court= arbitration_court,
                           name=name,
                           cabinet=cabinet,
                           day_name=day_name,
                           url=url)
            # judge.save()
            messages.success(request, 'Судья успешно добавлен!')
            return redirect('add_judge')  # Переадресация на ту же страницу
    else:
        form = JudgeFrom() # Если GET запрос, то возврат данных
        message = "Заполните поля судьи"

    return render(request, 'sheduleapp/judge_form.html', {'form':form,
                                                        "message": message})

# добавления сайта
@login_required
def add_site(request):
    if request.method == 'POST':
        form = SiteFrom(request.POST)
        message = 'Ошибка в заполнение данных'
        if form.is_valid():
            title = form.cleaned_data["title"]
            url = form.cleaned_data["url"]
            site = Site.objects.create(user=request.user,title= title, url=url)
            # site.save()
            messages.success(request, 'Сайт успешно добавлен!')
            return redirect('add_site')  # Переадресация на ту же страницу
    else:
        form = SiteFrom() # Если GET запрос, то возврат данных
        message = "Заполните поля сайта"

    return render(request, 'sheduleapp/site_form.html', {'form':form,
                                                        "message": message})

@login_required
def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            new_case = form.save(commit=False)  # Не сохранять сразу, чтобы можно было добавить пользователя
            new_case.user = request.user  # Автоматически устанавливаем текущего пользователя
            new_case.save()  # Теперь сохраняем запись
            return redirect('home')  # Переходим на главную страницу после успешного сохранения
    else:
        form = CaseForm()
    context = {'form': form}
    return render(request, 'sheduleapp/case_add.html', context)





# вывод всех дел, которые будут в ближайшее время
@login_required
def case_all_activ(request, status=None):
    today = date.today()
    # Получаем дату послезавтра и послепослезавтра
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    
    if status == 'active':
        cases = Case.objects.filter(case_activ='Активное', user=request.user)
        return render(request, 'sheduleapp/cases_activ_and_archiv.html', 
                      {"cases": cases, 'status':status})
    elif status == 'archive':
        cases = Case.objects.filter(case_activ='Архив', user=request.user)
        return render(request, 'sheduleapp/cases_activ_and_archiv.html', 
                      {"cases": cases, 'status':status})
    else:
        cases_today = Case.objects.filter(case_activ='Активное', event_date=today, user=request.user) 
        cases_tomorrow = Case.objects.filter(case_activ='Активное', event_date=tomorrow, user=request.user) 
        cases_day_after_tomorrow = Case.objects.filter(case_activ='Активное', event_date=day_after_tomorrow, user=request.user) 
        context = {
            'cases_today': cases_today,
            'cases_tomorrow': cases_tomorrow,
            'cases_day_after_tomorrow': cases_day_after_tomorrow,
            'today': today,
            'tomorrow': tomorrow,
            'day_after_tomorrow': day_after_tomorrow
        }
        return render(request, 'sheduleapp/case_user_activ.html', context)


# переход на конрекное дело
@login_required
def case_detail(request, case_number):
    case_detail = get_object_or_404(Case, number=case_number)
    context = {
        'case': case_detail
    }
    return render(request, 'sheduleapp/case_detail.html', context)


# Представление для удаления дела
@login_required
def delete_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('home')  # Переход на главную страницу после удаления
    context = {'case': case}
    return render(request, 'sheduleapp/case_confirm_delete.html', context)


# Представление для редактирования дела
@login_required
def edit_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    form = CaseForm(instance=case)
    
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {
        'form': form,
        'case': case,
    }
    return render(request, 'sheduleapp/case_edit_form.html', context)


# вывод всех судей, которые рассматривают дела сегодня
@login_required
def judge_full(request):
    today = date.today()
    dict_day = {0:"ПН", 1:"ВТ", 2:"СР", 3:"ЧТ", 4:"ПТ"}
    judges = Judges.objects.filter(day_name=dict_day.get(today.weekday()))
    now = datetime.now() # Преобразуем в нужный формат
    date_time_str = now.strftime("%Y-%m-%dT%H:%M:%S") # Кодируем строку для URL
    url_encoded_date_time = urllib.parse.quote(date_time_str)
    context = {"judges": judges,
               'today': today,
               'time': url_encoded_date_time}
    return render(request, 'sheduleapp/shedule_new_day.html', context)


# вывод меню для выбора открытие сайтов или расписаний
@login_required
def double_menu(request):
    return render(request, 'sheduleapp/double_menu.html')


# вывод всех судей, которые есть в БД для открытия двух окон одновременно
@login_required
def two_site_judge(request, id):
    # Разбиваем строку id на список целых чисел
    list_id = map(int, id.split('&'))

    # Получаем судей, соответствующих указанным ID и текущему пользователю
    judges = Judges.objects.filter(pk__in=list_id)
    now = datetime.now() # Преобразуем в нужный формат
    date_time_str = now.strftime("%Y-%m-%dT%H:%M:%S") # Кодируем строку для URL
    url_encoded_date_time = urllib.parse.quote(date_time_str)
    print(url_encoded_date_time)
    context = {'judges': judges, 'time':url_encoded_date_time}
    return render(request, 'sheduleapp/two_site_judge.html', context)

# вывод всех сайтов, которые есть в БД для открытия двух окон одновременно
@login_required
def two_site(request, id):
    list_id = id.split('&')
    list_id=list(int(x) for x in list_id)
    sites = Site.objects.filter(pk__in=list_id)
    context = {'sites': sites}
    return render(request, 'sheduleapp/two_site.html', context)


# вывод выбранных расписаний двух кабинетов в одном окне
@login_required
def judge_double_menu(request):
    if request.method == 'POST':
        form = JudgeMenu(user=request.user, data=request.POST)  # Передаем пользователя в форму
        message = ""
        if form.is_valid():
            selected_choices = form.cleaned_data['choices']
            if len(selected_choices) != 2:
                message = "Пожалуйста, выберите ровно два варианта."
            else:
                # Преобразуем объекты в список идентификаторов
                selected_ids = [choice.id for choice in selected_choices]
                # Формируем строку параметров для передачи на другой сайт
                params = '&'.join(f'{id}' for id in selected_ids)
                # Переходим на новый сайт с параметрами
                return redirect('two_site_judge', id=params)
    else:
        form = JudgeMenu(user=request.user)  # Передаем пользователя в форму
        message = ""
    return render(request, 'sheduleapp/double_menu_judge.html', {'form':form,
                                                        "message": message})

# вывод выбранных двух сайтов в одном окне
@login_required
def site_double_menu(request):
    if request.method == 'POST':
        form = SiteMenu(user=request.user,
                         data=request.POST)
        message = ""
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
        form = SiteMenu(user=request.user)
        message = ""
    return render(request, 'sheduleapp/double_menu_site.html', {'form':form,
                                                        "message": message})
