import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput

from .models import Judges, Site, Profile


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


class SiteFrom(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                 "placeholder":" Напишите  "
                                                      "Названия сайта"}))
    url = forms.URLField(widget=forms.TextInput(attrs={"class":
                                                            "form-control",
                                                 "placeholder":" Напишите  "
                                                      "адрес (URL) сайта"}))



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


class JudgeMenu(forms.Form):
    choices = forms.ModelMultipleChoiceField(queryset=Judges.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    def clean_options(self):
        selected_choices = self.cleaned_data['choices']
        if len(selected_choices) > 1:
            raise forms.ValidationError(
                "Пожалуйста, выберите ровно два варианта.")
        return selected_choices

class SiteMenu(forms.Form):
    choices = forms.ModelMultipleChoiceField(queryset=Site.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def clean_options(self):
        selected_choices = self.cleaned_data['choices']
        if len(selected_choices) > 1:
            raise forms.ValidationError(
                "Пожалуйста, выберите ровно два варианта.")
        return selected_choices