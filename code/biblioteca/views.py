from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Livro, Exemplar, Emprestimo
from django.shortcuts import redirect
from django.contrib import messages

@login_required(login_url="/auth/login")
def livros(request):
    livros = Livro.objects.annotate(
        exemplares_disponiveis=Count(
            'exemplar',
            filter=Q(exemplar__status=Exemplar.StatusType.DISPONIVEL)
        )
    ).order_by('-exemplares_disponiveis', 'titulo')
    context = {
        'livros': livros
    }
    template = loader.get_template('livros.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url="/auth/login")
def reservar(request, livro_id):
    if request.method == "POST":
        try:
            exemplar = Exemplar.objects.filter(livro_id=livro_id, status=Exemplar.StatusType.DISPONIVEL).first()

            if exemplar:
                emprestimo = Emprestimo.objects.create(
                    usuario=request.user,
                    exemplar=exemplar
                )

                exemplar.status = Exemplar.StatusType.EMPRESTADO
                exemplar.save()

        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")

    return redirect('livros')


