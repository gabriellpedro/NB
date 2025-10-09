from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("populate-baralho/", views.populate_baralho_cadastro, name="populate-baralho"),
    path("jogador/criar/", views.CriarJogadorView.as_view(), name="criar-jogador"),
    path(
        "jogador/<int:id_jogador>/",
        views.JogadorDetalhesView.as_view(),
        name="jogador-detalhes",
    ),
    path(
        "jogador/<int:id_jogador>/esquerda/",
        views.jogador_esquerda,
        name="jogador_esquerda",
    ),
    path(
        "jogador/<int:id_jogador>/direita/",
        views.jogador_direita,
        name="jogador_direita",
    ),
    path(
        "jogador/<int:id_jogador>/cartas/",
        views.CartasJogadorView.as_view(),
        name="cartas_jogador",
    ),
    path(
        "partida/<int:id_partida>/jogadores/",
        views.JogadoresPartidaView.as_view(),
        name="jogadores_partida",
    ),
    path(
        "popular-tabuleiro/",
        views.PopularTabuleiroView.as_view(),
        name="popular_tabuleiro",
    ),
    path("rolar-dado/", views.RolarDadoView.as_view(), name="rolar_dado"),
    path("executar-acao-casa/", views.executar_acao_casa, name="executar-acao-casa"),
    path(
        "notificacoes/partida/<int:partida_id>/",
        views.notificacoes_pendentes_partida,
        name="notificacoes_partida",
    ),
    path(
        "notificacoes/jogador/<int:jogador_id>/partida/<int:partida_id>/",
        views.notificacoes_pendentes_jogador,
        name="notificacoes_jogador",
    ),
    path(
        "notificacoes/processar/",
        views.marcar_notificacao_processada,
        name="marcar_notificacao_processada",
    ),
    # ControleJogador
    path(
        "atualizar-controle-jogador/",
        views.atualizar_controle_jogador,
        name="atualizar_controle_jogador",
    ),
    path(
        "consultar-controle-jogador/<int:id_jogador>/<int:id_partida>/",
        views.consultar_controle_jogador,
        name="consultar_controle_jogador",
    ),
    path(
        "decrementar-controle-jogador/",
        views.decrementar_controle_jogador_campo,
        name="decrementar_controle_jogador",
    ),
    # Cartas em Evidência
    path(
        "alterar-carta-evidencia/",
        views.atualizar_cartas_baralho,
        name="alterar_carta_evidencia",
    ),
    path("consulta-carta-evidencia/<int:id_jogador>",
         views.consultar_cartas_evidencia,
         name="consultar_cartas_evidencia"),
    path(
        "jogador/<int:id_jogador>/descartar-carta/<int:id_carta>/",
        views.descartar_carta_por_id,
        name="descartar_carta_por_id",
    ),
    path(
        "criar-elogio/",
        views.criar_elogio,
        name="criar_elogio",
    ),
    path(
        "partida/<int:id_partida>/elogios/",
        views.listar_elogios_partida,
        name="listar_elogios_partida",
    ),
]
