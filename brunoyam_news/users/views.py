from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView
from django.urls import reverse_lazy

from .forms import SignUpForm, LoginForm, PersonalDataForm
from .models import User


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PersonalDataView(DetailView):
    template_name = 'personal.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.request.user.id)


class PersonalDataUpdateView(FormView):
    form_class = PersonalDataForm
    template_name = 'personal_data_change.html'
    success_url = reverse_lazy('personal')

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def form_valid(self, form):
        user = self.get_object()
        cleaned_data = form.cleaned_data
        user.name = cleaned_data['name']
        user.surname = cleaned_data['surname']
        user.email = cleaned_data['email']
        user.save()
        return super().form_valid(form)