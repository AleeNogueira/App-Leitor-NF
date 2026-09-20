

from django.urls import path
from app import views as app_views

urlpatterns = [
    path("", app_views.upload_nota_fiscal, name="upload_nota_fiscal"),
    
    path("confirmar/", app_views.confirmar_nota_fiscal, name="confirmar_nota_fiscal"),
]