from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import NotasENEM

def index(request):
    return render(request, 'index.html')

def registrar(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Usuário já cadastrado.')
            return redirect('registrar')
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        return redirect('login')
    return render(request, 'registrar.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
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
    if request.method == 'POST':
        notas, created = NotasENEM.objects.get_or_create(user=request.user)
        notas.linguagens_nota = float(request.POST['linguagens_nota'])
        notas.linguagens_peso = float(request.POST['linguagens_peso'])
        notas.matematica_nota = float(request.POST['matematica_nota'])
        notas.matematica_peso = float(request.POST['matematica_peso'])
        notas.natureza_nota = float(request.POST['natureza_nota'])
        notas.natureza_peso = float(request.POST['natureza_peso'])
        notas.humanas_nota = float(request.POST['humanas_nota'])
        notas.humanas_peso = float(request.POST['humanas_peso'])
        notas.redacao_nota = float(request.POST['redacao_nota'])
        notas.redacao_peso = float(request.POST['redacao_peso'])
        notas.save()
        return redirect('resultado')
    return render(request, 'inserir_notas.html')

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
