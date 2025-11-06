from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('livros', views.livros, name='livros'),
    path('livros/<int:livro_id>/reservar/', views.reservar, name='reservar'),
    path('emprestimos', views.emprestimos, name='emprestimos'),
    path('emprestimos/<int:emprestimo_id>/devolver/', views.devolver, name='devolver'),
    path('multas', views.multas, name='multas'),
    path('multas/<int:multa_id>/pagar/', views.pagar, name='pagar'),
    path('perfil', views.perfil, name='perfil'),
    path('perfil/alterar/', views.alterar_perfil, name='alterar_perfil'),
    path('', RedirectView.as_view(url='livros')),
]