from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inserir_notas/', views.inserir_notas, name='inserir_notas'),
    path('resultado/', views.resultado, name='resultado'),
    path('logout/', views.logout_view, name='logout'),
]
