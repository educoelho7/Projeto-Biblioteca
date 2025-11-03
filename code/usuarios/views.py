from .models import Usuario
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.shortcuts import redirect
import re

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        if user:
            login_django(request, user)
            return redirect('livros')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
            return render(request, 'login.html')

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else: 
        usuario = request.POST.get('usuario')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmarsenha = request.POST.get('confirmar_senha')
        telefone = request.POST.get('telefone')
        
        if senha != confirmarsenha:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'cadastro.html')

        user = Usuario.objects.filter(username=usuario).first()
        if user:
            messages.error(request, 'Já existe um usuário com esse nome. Tente novamente.')
            return render(request, 'cadastro.html')
        
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Já existe uma conta com esse e-mail.')
            return render(request, 'cadastro.html')
        
        if not re.match(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', telefone):
            messages.error(request, "Telefone inválido. Use o formato (99) 99999-9999.")
            return render(request, 'cadastro.html')

        user = Usuario.objects.create_user(
            username=usuario,
            first_name=nome, 
            last_name=sobrenome, 
            email=email, 
            password=senha, 
            telefone=telefone)
        user.save()
        
        messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return redirect('login')
    
def logout(request):
    logout_django(request)
    return redirect('login')


