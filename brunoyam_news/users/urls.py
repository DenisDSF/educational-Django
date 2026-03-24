from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView)
from django.urls import path, reverse_lazy

from .forms import MyPasswordChangeForm
from .views import (
    sign_up_view,
    LoginUser,
    logout_view,
    personal_view,
    personal_data_change_view
)

urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('personal/', personal_view, name='personal'),
    path(
        'personal/change/',
        personal_data_change_view,
        name='personal_data_change'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            form_class = MyPasswordChangeForm,
            success_url = reverse_lazy('password_change_done'),
            template_name = 'password_change.html'
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),
]

