from django.db.models import Count, Q, F, OrderBy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.loader import render_to_string
from .models import Livro, Exemplar, Emprestimo, Multa
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from .constants import QTD_MAXIMA_DIAS_DEVOLUCAO, VALOR_BASE_MULTA, VALOR_POR_DIA_ATRASO

@login_required(login_url="/auth/login")
def livros(request):
    query = request.GET.get("q", "")
    livros = Livro.objects.annotate(
        exemplares_disponiveis=Count(
            'exemplar',
            filter=Q(exemplar__status=Exemplar.StatusType.DISPONIVEL)
        )
    ).order_by('-exemplares_disponiveis', 'titulo')
    if query:
        livros = livros.filter(titulo__icontains=query)
    paginator = Paginator(livros, 10)
    page_number = request.GET.get('page')
    livros = paginator.get_page(page_number)
    context = {
        'livros': livros,
        'query': query,
    }
    if request.htmx:
        return render(request, "partials/lista_livros.html", context)
    
    return render(request, "livros.html", context)

@login_required(login_url="/auth/login")
def reservar(request, livro_id):
    if request.method == "POST":
        try:
            exemplar = Exemplar.objects.filter(livro_id=livro_id, status=Exemplar.StatusType.DISPONIVEL).first()
            multas = Multa.objects.filter(emprestimo__usuario=request.user, status=Multa.StatusType.EM_ABERTO)
            livro = Livro.objects.get(id=livro_id)
            if exemplar and not multas:
                emprestimo = Emprestimo.objects.create(
                    usuario=request.user,
                    exemplar=exemplar
                )

                exemplar.status = Exemplar.StatusType.EMPRESTADO
                exemplar.save()
            
            livros = Livro.objects.annotate(
                exemplares_disponiveis=Count(
                    'exemplar',
                    filter=Q(exemplar__status=Exemplar.StatusType.DISPONIVEL)
                )
            ).order_by('-exemplares_disponiveis', 'titulo')

            paginator = Paginator(livros, 10)
            page_number = request.GET.get('page')
            livros = paginator.get_page(page_number)
            
            

            html = render_to_string("partials/lista_livros.html", {
                "livros": livros,
                "query": ""
            }, request=request)

        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")
        
        return HttpResponse(html)

    return redirect('livros')


@login_required(login_url="/auth/login")
def emprestimos(request):
    emprestimos = Emprestimo.objects.filter(usuario=request.user).order_by(
        OrderBy(F('data_devolucao'), nulls_first=True),
        "-data_emprestimo"
    )

    paginator = Paginator(emprestimos, 10)
    page_number = request.GET.get("page")
    emprestimos = paginator.get_page(page_number)
    
    return render(request, "emprestimos.html", {"emprestimos": emprestimos})

@login_required(login_url="/auth/login")
def devolver(request, emprestimo_id):
    if request.method == "POST":
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()
        dias = (emprestimo.data_devolucao - emprestimo.data_emprestimo).days
        atraso = dias - QTD_MAXIMA_DIAS_DEVOLUCAO
        if atraso > 0:
            Multa.objects.create(
                emprestimo=emprestimo,
                valor=VALOR_BASE_MULTA+VALOR_POR_DIA_ATRASO*atraso,
                status=Multa.StatusType.EM_ABERTO
            )

        emprestimo.exemplar.status = Exemplar.StatusType.DISPONIVEL
        emprestimo.exemplar.save()
        return JsonResponse({'atraso': atraso})

    return JsonResponse({'error': 'Método inválido'}, status=400)

@login_required(login_url="/auth/login")
def multas(request):
    multas = Multa.objects.filter(emprestimo__usuario=request.user).order_by("-emprestimo__data_devolucao")

    paginator = Paginator(multas, 10)
    page_number = request.GET.get("page")
    multas = paginator.get_page(page_number)
    
    return render(request, "multas.html", {"multas": multas})

@login_required(login_url="/auth/login")
def pagar(request, multa_id):
    if request.method == "POST":
        multa = Multa.objects.get(id=multa_id)
        multa.status = Multa.StatusType.PAGA
        multa.save()
    
    return redirect('multas')

@login_required(login_url="/auth/login")
def pagar(request, multa_id):
    if request.method == "POST":
        multa = Multa.objects.get(id=multa_id)
        multa.status = Multa.StatusType.PAGA
        multa.save()
    
    return redirect('multas')

@login_required(login_url="/auth/login")
def perfil(request):
    return render(request, 'profile.html', {
        'user': request.user
    })

@login_required(login_url="/auth/login")
def alterar_perfil(request):
    user = request.user

    if request.method == 'POST':
        password = request.POST.get('senha')

        # Verify the password
        if not user.check_password(password):
            message = "Senha incorreta. As alterações não foram salvas."
            return render(request, 'profile.html', {'user': user, 'message': message})

        # If password is correct, update the fields
        user.first_name = request.POST.get('nome', user.first_name)
        user.last_name = request.POST.get('sobrenome', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.telefone = request.POST.get('telefone', user.telefone)
        
        nova_senha = request.POST.get('nova-senha', '')
        if nova_senha:
            user.set_password(nova_senha)
            user.save()
            update_session_auth_hash(request, user)
        else:
            user.save()

        message = "Perfil atualizado com sucesso!"
        return render(request, 'profile.html', {'user': user, 'message': message})

    return render(request, 'profile.html', {'user': user })
