from django.urls import path
from .views import (
    chat_view,
    chat_send_view,
    cookie_policy_view,
    data_policy_view,
    home,
    terms_view,
)
from users.views import signup_view, login_view
urlpatterns = [
    path("", home, name="home"),
    path("terms/", terms_view, name="terms"),
    path("data-policy/", data_policy_view, name="data_policy"),
    path("cookie-policy/", cookie_policy_view, name="cookie_policy"),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('chat/', chat_view, name='chat'),
    path('chat/send/', chat_send_view, name='chat_send'),
]
