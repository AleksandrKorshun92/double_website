from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Вход после регистрации
#             return redirect('home')  # Замените 'home' на ваш маршрут
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})
#
# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Замените 'home' на ваш маршрут
#     else:
#         form = UserLoginForm()
#     return render(request, 'accounts/login.html', {'form': form})