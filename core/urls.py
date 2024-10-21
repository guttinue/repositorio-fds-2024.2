from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inserir_notas/', views.inserir_notas, name='inserir_notas'),
    path('logout/', views.logout_view, name='logout'),
    path('cursos_recomendados/', views.cursos_recomendados, name='cursos_recomendados'),
    path('historico/', views.historico, name='historico'),
    path('rotina_personalizada/', views.rotina_personalizada, name='rotina_personalizada'),
    path('historico/', views.historico, name='historico'),
    path('excluir_nota/<int:nota_id>/', views.excluir_nota, name='excluir_nota'),
    path('resultado/<int:nota_id>/', views.resultado, name='resultado'),

]
