from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

import random

from .models import OneTimeCode
from .forms import SignUpForm


def o_t_code_send(user, to_email):
    code_create = OneTimeCode.objects.create(user_id=user, code=random.randint(100000, 999999))
    code_ = OneTimeCode.objects.filter(user_id=user).values_list('code', flat=True)
    for code in code_:
        print(code_)

        subject = f'Ваш код подтверждения:'
        text_content = (
            f'{code}<br>'
        )
        html_content = (
            f'{code}<br>'
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            authenticated = Group.objects.get(name="authenticated")
            user.groups.add(authenticated)
            to_email = form.cleaned_data.get('email')
            o_t_code_send(user.id, to_email)

            return redirect("signup/code")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@csrf_protect
def o_t_code_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        code = request.POST.get('code')
        user_id = User.objects.get(username=username)
        if OneTimeCode.objects.filter(code=code, user__username=username).exists():
            User.objects.filter(username=username).update(is_active=True)
            login(request, user_id)
            return redirect("http://127.0.0.1:8000/announcements")
        else:
            return HttpResponse('Invalid code')

    return render(request, 'registration/o_t_code_send_confirm.html')


@csrf_protect
def o_t_code_send_again(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email) is not None:
            id_ = User.objects.filter(email=email).values_list('id', flat=True)
            for item in id_:
                if OneTimeCode.objects.filter(user_id=item) is None:
                    o_t_code_send(item, email)
                    return redirect("http://127.0.0.1:8000/accounts/signup/code")
                else:
                    return HttpResponse('Ваш прошлый код ещё действует!')
            else:
                return HttpResponse('Указанная почта не проходила регистрацию!')

    return render(request, 'registration/o_t_code_send_again.html')
