from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
        path('', dashboard, name='dashboard'),

]