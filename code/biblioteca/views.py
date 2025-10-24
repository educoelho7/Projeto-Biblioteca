from django.db.models import Count, Q
from django.http import HttpResponse
from django.template import loader
from .models import Livro
from .models import Exemplar

def livros(request):
    livros = Livro.objects.annotate(
        exemplares_disponiveis=Count(
            'exemplar',
            filter=Q(exemplar__status=Exemplar.StatusType.DISPONIVEL)
        )
    )
    context = {
        'livros': livros
    }
    template = loader.get_template('livros.html')
    return HttpResponse(template.render(context, request))
