from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_request, name="giris"),
    path("register", views.register_request, name="kayit"),
    path("logout", views.logout_request, name="cikis")
]