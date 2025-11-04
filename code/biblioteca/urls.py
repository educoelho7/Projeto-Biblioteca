from django.urls import path
from . import views

urlpatterns = [
    path('livros', views.livros, name='livros'),
    path('livros/<int:livro_id>/reservar/', views.reservar, name='reservar'),
    path('emprestimos', views.emprestimos, name='emprestimos'),
    path('devolver/<int:emprestimo_id>/', views.devolver_exemplar, name='devolver_exemplar'),
    path('multas', views.multas, name='multas'),
    path('multas/<int:multa_id>/pagar', views.pagar, name='pagar'),
]