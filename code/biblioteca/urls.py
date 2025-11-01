from django.urls import path
from . import views

urlpatterns = [
    path('livros', views.livros, name='livros'),
    path('livros/<int:livro_id>/reservar/', views.reservar, name='reservar'),

]