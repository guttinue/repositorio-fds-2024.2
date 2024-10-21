from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import NotasENEM

def index(request):
    return render(request, 'index.html')

def registrar(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        password = request.POST['password']
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome de usuário já cadastrado.')
            return redirect('registrar')
        user = User.objects.create_user(username=nome, password=password)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        return redirect('login')
    return render(request, 'registrar.html')


def login_view(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        password = request.POST['password']
        user = authenticate(request, username=nome, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciais inválidas.')
            return redirect('login')
    return render(request, 'login.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

def inserir_notas(request):
    if not request.user.is_authenticated:
        return redirect('login')
    disciplinas = [
        {'nome': 'Linguagens, Códigos e suas Tecnologias', 'campo_nota': 'linguagens_nota', 'campo_peso': 'linguagens_peso'},
        {'nome': 'Matemática e suas Tecnologias', 'campo_nota': 'matematica_nota', 'campo_peso': 'matematica_peso'},
        {'nome': 'Ciências da Natureza e suas Tecnologias', 'campo_nota': 'natureza_nota', 'campo_peso': 'natureza_peso'},
        {'nome': 'Ciências Humanas e suas Tecnologias', 'campo_nota': 'humanas_nota', 'campo_peso': 'humanas_peso'},
        {'nome': 'Redação', 'campo_nota': 'redacao_nota', 'campo_peso': 'redacao_peso'},
    ]
    if request.method == 'POST':
        notas, created = NotasENEM.objects.get_or_create(user=request.user)
        for disciplina in disciplinas:
            nota = float(request.POST[disciplina['campo_nota']])
            peso = float(request.POST[disciplina['campo_peso']])
            setattr(notas, disciplina['campo_nota'], nota)
            setattr(notas, disciplina['campo_peso'], peso)
        notas.save()
        return redirect('resultado')
    return render(request, 'inserir_notas.html', {'disciplinas': disciplinas})

def resultado(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        notas = NotasENEM.objects.get(user=request.user)
        media_ponderada = notas.calcular_media_ponderada()
        context = {
            'notas': notas,
            'media_ponderada': media_ponderada,
        }
        return render(request, 'resultado.html', context)
    except NotasENEM.DoesNotExist:
        messages.error(request, 'Você ainda não inseriu suas notas.')
        return redirect('inserir_notas')

def logout_view(request):
    logout(request)
    return redirect('login')
