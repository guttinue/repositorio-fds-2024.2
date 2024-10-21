from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import NotasENEM
from django.db.models import Avg
from .models import NotasENEM, Curso
from django.contrib.auth.decorators import login_required

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
        {'nome': 'Linguagens', 'campo_nota': 'linguagens_nota'},
        {'nome': 'Matemática', 'campo_nota': 'matematica_nota'},
        {'nome': 'Natureza', 'campo_nota': 'natureza_nota'},
        {'nome': 'Humanas', 'campo_nota': 'humanas_nota'},
        {'nome': 'Redação', 'campo_nota': 'redacao_nota'},
    ]
    cursos = Curso.objects.all()
    if request.method == 'POST':
        curso_id = request.POST['curso']
        curso = Curso.objects.get(id=curso_id)
        notas = NotasENEM(user=request.user, curso=curso)
        for disciplina in disciplinas:
            nota = float(request.POST[disciplina['campo_nota']])
            setattr(notas, disciplina['campo_nota'], nota)
        notas.save()
        return redirect('historico')
    return render(request, 'inserir_notas.html', {'disciplinas': disciplinas, 'cursos': cursos})



@login_required
def resultado(request, nota_id):
    try:
        notas = NotasENEM.objects.get(id=nota_id, user=request.user)
        media_ponderada = notas.calcular_media_ponderada()
        context = {
            'notas': notas,
            'media_ponderada': media_ponderada,
        }
        return render(request, 'resultado.html', context)
    except NotasENEM.DoesNotExist:
        messages.error(request, 'Notas não encontradas.')
        return redirect('historico')



def logout_view(request):
    logout(request)
    return redirect('login')

def historico(request):
    notas_list = NotasENEM.objects.filter(user=request.user).order_by('-data_criacao')
    return render(request, 'historico.html', {'notas_list': notas_list})

def rotina_personalizada(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'rotina_personalizada.html')

from django.shortcuts import render, redirect
from .models import Curso
from django.contrib import messages

def cursos_recomendados(request):
    if not request.user.is_authenticated:
        return redirect('login')
    disciplinas = [
        {'nome': 'Linguagens', 'campo_nota': 'linguagens_nota'},
        {'nome': 'Matemática', 'campo_nota': 'matematica_nota'},
        {'nome': 'Natureza', 'campo_nota': 'natureza_nota'},
        {'nome': 'Humanas', 'campo_nota': 'humanas_nota'},
        {'nome': 'Redação', 'campo_nota': 'redacao_nota'},
    ]
    if request.method == 'POST':
        try:
            linguagens_nota = float(request.POST['linguagens_nota'])
            matematica_nota = float(request.POST['matematica_nota'])
            natureza_nota = float(request.POST['natureza_nota'])
            humanas_nota = float(request.POST['humanas_nota'])
            redacao_nota = float(request.POST['redacao_nota'])
        except (ValueError, KeyError):
            messages.error(request, 'Por favor, insira todas as notas corretamente.')
            return render(request, 'cursos_recomendados.html', {'disciplinas': disciplinas})

        cursos = Curso.objects.all()
        recomendacoes = []

        for curso in cursos:
            soma_notas_pesos = (
                linguagens_nota * curso.linguagens_peso +
                matematica_nota * curso.matematica_peso +
                natureza_nota * curso.natureza_peso +
                humanas_nota * curso.humanas_peso +
                redacao_nota * curso.redacao_peso
            )
            soma_pesos = (
                curso.linguagens_peso +
                curso.matematica_peso +
                curso.natureza_peso +
                curso.humanas_peso +
                curso.redacao_peso
            )
            media_ponderada = soma_notas_pesos / soma_pesos if soma_pesos else 0

            recomendacoes.append({
                'curso': curso.nome,
                'media_ponderada': media_ponderada,
            })

        recomendacoes.sort(key=lambda x: x['media_ponderada'], reverse=True)

        context = {
            'recomendacoes': recomendacoes,
        }
        return render(request, 'cursos_recomendados_resultado.html', context)
    return render(request, 'cursos_recomendados.html', {'disciplinas': disciplinas})


def historico(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notas_list = NotasENEM.objects.filter(user=request.user).order_by('-data_criacao')
    return render(request, 'historico.html', {'notas_list': notas_list})

@login_required
def excluir_nota(request, nota_id):
    try:
        nota = NotasENEM.objects.get(id=nota_id, user=request.user)
        nota.delete()
        messages.success(request, 'Entrada excluída com sucesso.')
    except NotasENEM.DoesNotExist:
        messages.error(request, 'Entrada não encontrada.')
    return redirect('historico')


