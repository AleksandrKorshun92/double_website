"""
Определяем основные формы проекта (сайта):
- форма по добавлению судьи
- форма по добавлению сайта
- форма регистрации пользователя
- форма для просмотра двух расписаний судей
- форма для просмотра двух сайтов
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
import datetime
from .models import Judges, Site, Case

#форма по добавлению судьи в БД
class JudgeFrom(forms.Form):
    arbitration_court = forms.ChoiceField(choices=
                                          [('АС СПб', 'Арбитражный суд Санкт-Петербурга и Ленинградской области'),
                                            ('13 ААС', '13 Арбитражный суд')])
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                 "placeholder":" Напишите  "
                                                      "Фамилию судьи "}))
    cabinet = forms.IntegerField(min_value=100, widget=forms.NumberInput(
        attrs={"class": "form-control", "placeholder":" Напишите  "
                                                      "номер кабинета" }))
    day_name = forms.ChoiceField(choices=
                                          [('ПН', 'Понедельник'),
                                            ('ВТ', 'Вторник'),
                                           ('СР', 'Среда'),
                                           ('ЧТ', 'Четверг'),
                                           ('Пт', 'Пятница')
                                           ])

#форма по добавлению сайта в БД
class SiteFrom(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                 "placeholder":" Напишите  "
                                                      "названия сайта"}))
    url = forms.URLField(widget=forms.TextInput(attrs={"class":
                                                            "form-control",
                                                 "placeholder":" Напишите  "
                                                      "адрес (URL) сайта"}))


#форма по добавлению дела
class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields =['number','court', 'court', 'costumer', 'costumer_status', 'other_costumer', 
                 'event', 'event_date', 'description_case', 'case_activ'] 
        labels = {
            'number': 'Номер дела',
            'court': 'Суд',
            'costumer': 'Заказчик',
            'costumer_status': 'Роль заказчика',
            'other_costumer': 'Другая сторона',
            'event': 'Событие',
            'event_date': 'Дата события',
            'description_case': 'Описание дела',
            'case_activ': 'Статус дела',
        }
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напишите номер дела'}),
            'court': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напишите название суда'}),
            'costumer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напишите заказчика'}),
            'costumer_status': forms.Select(choices=[('Истец', 'Истец'), ('Ответчик', 'Ответчик')]),
            'other_costumer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напишите другую сторону'}),
            'event': forms.Select(choices=[
                ('Претензия', 'Претензия'),
                ('Иск', 'Иск'),
                ('Отзыв', 'Отзыв'),
                ('Возражение', 'Возражение'),
                ('Судебное заседание', 'Судебное заседание'),
                ('Апелляционая жалоба', 'Апелляционая жалоба'),
                ('Кассационная жалоба', 'Кассационная жалоба'),
                ('Судебные расходы', 'Судебные расходы'),
                ('Иное', 'Иное')
            ]),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Напишите дату и время события'}),
            'description_case': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напишите короткую информацию и план по делу'}),
            'case_activ': forms.Select(choices=[('Активное', 'Активное'), ('Архив', 'Архив')])
        }

#форма для регистрации пользователя в БД
class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(initial=datetime.date.today,
                                 widget=forms.DateInput(
                                     attrs={'class': 'form-control',
                                            'type': 'date'}))
    bio = forms.CharField(max_length=200)

    class Meta:
        model = get_user_model()
        fields = ['username', 'last_name', 'email', "birth_date", 'bio']

        labels = {"username": "Логин",
                  'email': 'Почта', 'last_name': 'Ваше имя',
                  "birth_date": "Дата рождения", "bio": "Напишите коротко о "
                                                        "себе"}
        widgets = {"username": forms.TextInput(attrs={"class": "form-input"}),
                   "last_name": forms.TextInput(attrs={"class": "form-input"}),
                   'email': forms.EmailInput(attrs={"class": "form-input"})
                   }


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data


#форма для выбора кабинета судьи
class JudgeMenu(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Judges.objects.none(),  # Изначально пустой queryset
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, user=None, *args, **kwargs):
        super(JudgeMenu, self).__init__(*args, **kwargs)
        if user is not None:
            # Фильтруем судей по текущему пользователю
            self.fields['choices'].queryset = Judges.objects.filter(user=user)



#форма для выбора сайта
class SiteMenu(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Site.objects.none(),  # Изначально пустой queryset
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, user=None, *args, **kwargs):
        super(SiteMenu, self).__init__(*args, **kwargs)
        if user is not None:
            # Фильтруем судей по текущему пользователю
            self.fields['choices'].queryset = Site.objects.filter(user=user)
