

from django.urls import path
from app import views as app_views

urlpatterns = [
    path("login/", app_views.login_view, name="login"),
    path("logout/", app_views.logout_view, name="logout"),
    path("", app_views.upload_nota_fiscal, name="upload_nota_fiscal"),
]