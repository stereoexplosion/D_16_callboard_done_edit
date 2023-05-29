from django.urls import path
from .views import signup, o_t_code_login, o_t_code_send_again

urlpatterns = [
    path('signup', signup, name='signup'),
    path('signup/code/again', o_t_code_send_again, name='code_again'),
    path('signup/code', o_t_code_login, name='code'),
]
