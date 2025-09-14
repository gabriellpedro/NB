from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("populate-baralho/", views.populate_baralho_cadastro, name="populate-baralho"),
    path('jogador/criar/', views.CriarJogadorView.as_view(), name="criar-jogador"),
    path("jogador/<int:id_jogador>/", views.JogadorDetalhesView.as_view(), name="jogador-detalhes"),
]
