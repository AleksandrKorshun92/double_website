from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages


from .tasks import send_registration_email, send_password_reset_email
from .forms import RegistrationForm
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

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
                send_registration_email.delay(user.pk)
                                               
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
    user = request.user  # Получаем текущего пользователя
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)


# вход (аутентификация)
def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']  # Используем имя поля form
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # перенаправляем на главную страницу
        else:
            messages.error(request,"Нет такого пользователя. Пройдите регистрацию.")
            return redirect('login')  # возвращаем обратно на страницу входа
    return render(request, 'registration/login.html')


class CustomPasswordResetView(auth_views.PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return super().form_valid(form)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)  # Получаем текущую информацию о сайте
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'https' if self.request.is_secure() else 'http'

        subject = 'Сброс пароля'
        context = {
            'domain':domain,
            'email': user.email,
            'uid': uid,
            'token': token,
            'protocol':protocol,
            'site_name': site_name
            
        }
        html_message = render_to_string('registration/password_reset_email.txt', context)
    
        # Вызовите задачу отправки письма
        send_password_reset_email.delay(user.email, subject, html_message)
        return redirect('done/')
