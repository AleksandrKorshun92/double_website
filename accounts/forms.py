from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=DateInput(), label='Дата рождения')
     
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


