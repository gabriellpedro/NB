from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("populate-baralho/", views.populate_baralho_cadastro, name="populate-baralho"),
    path('jogador/criar/', views.CriarJogadorView.as_view(), name="criar-jogador"),
    path("jogador/<int:id_jogador>/", views.JogadorDetalhesView.as_view(), name="jogador-detalhes"),
    path("popular-tabuleiro/", views.PopularTabuleiroView.as_view(), name="popular_tabuleiro"),
    path("rolar-dado/", views.RolarDadoView.as_view(), name="rolar_dado"),
    path("executar-acao-casa/", views.executar_acao_casa, name="executar-acao-casa"),
]
