from .models import Usuario
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse

def login(request):
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
        telefone = request.POST.get('telefone')

        user = Usuario.objects.filter(username=usuario).first()
        if user:
            messages.error(request, 'Já existe um usuário com esse nome. Tente novamente.')
            return render(request, 'cadastro.html')

        user = Usuario.objects.create_user(
            username=usuario,
            first_name=nome, 
            last_name=sobrenome, 
            email=email, 
            password=senha, 
            telefone=telefone)
        user.save()
        
        return render(request, 'login.html')
