from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm, LoginForm, PersonalDataForm
from .models import User


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def personal_view(request):
    user = get_object_or_404(User, id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'personal.html', context)

def personal_data_change_view(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user.name = cleaned_data['name']
            user.surname = cleaned_data['surname']
            user.email = cleaned_data['email']
            user.save()
            return redirect('personal')
    else:
        form = PersonalDataForm()
    return render(request, 'personal_data_change.html', {'form': form})