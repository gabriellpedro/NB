import json
import random
import traceback
from urllib.request import Request
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import (
    AcaoCadastro,
    Baralho,
    BaralhoCadastro,
    ControleJogador,
    ControlePartida,
    Elogio,
    Jogador,
    Notificacao,
    Partida,
    TabuleiroCadastro,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import api_view
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt


def populate_baralho_cadastro(request):
    if BaralhoCadastro.objects.exists():
        return JsonResponse({"message": "Tabela já populada!"}, status=200)

    info_cards = {
        1: {
            "nome_carta": "Bullying Verbal | Início | ID: 1",
            "descricao_carta": "Ao longe, você consegue escutar algumas pessoas rindo e comentando de alguém com o apelido... - O que você faz",
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        2: {
            "nome_carta": "Bullying Verbal | Início | ID: 2",
            "descricao_carta": "um colega de sua sala chega em você e comenta sobre o peso de outra colega com um tom debochado e humilhando ela - O que você faz",
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        3: {
            "nome_carta": "Bullying Verbal | Início | ID: 3",
            "descricao_carta": 'Enquanto você jogava futebol escutou o time adversário comentando o quão "perna de pau" você é" lá - O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        4: {
            "nome_carta": "Bullying Verbal | Início | ID: 4",
            "descricao_carta": 'Um trio de meninos chega em você e pergunta qual foi o acidente que fez sua cara ficar "assim" e saem rindo" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        5: {
            "nome_carta": "Bullying Verbal | Início | ID: 5",
            "descricao_carta": 'seus amigos comentam sobre a aparência de uma pessoa que você não é tão próxima" - O que você faz',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        6: {
            "nome_carta": "Bullying Verbal | Meio | ID: 6",
            "descricao_carta": "...Você fala com o grupo e tenta argumentar contra essa ação..",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        7: {
            "nome_carta": "Bullying Verbal | Meio | ID: 7",
            "descricao_carta": "… ignorar o comentário...Porém! Cada dia fica cada vez pior ",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        8: {
            "nome_carta": "Bullying Verbal | Meio | ID: 8",
            "descricao_carta": "...Você não tem coragem de contrariá-los, Porém",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        9: {
            "nome_carta": "Bullying Verbal | Meio | ID: 9",
            "descricao_carta": "...O grupo não gostou nada de você contrariá-los…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        10: {
            "nome_carta": "Bullying Verbal | Meio | ID: 10",
            "descricao_carta": "...Após tanto debate sobre o assunto as pessoas acabam concordando com sua argumentação…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        11: {
            "nome_carta": "Bullying Verbal | Meio | ID: 11",
            "descricao_carta": "... Após piora, você decide tomar uma providência e conversar com as pessoas...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        12: {
            "nome_carta": "Bullying Verbal | Meio | ID: 12",
            "descricao_carta": "...Após tentar, você apenas se afasta das pessoas que fizeram esse comentário...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        13: {
            "nome_carta": "Bullying Físico | Início | ID: 13",
            "descricao_carta": '"Você sente seu cabelo ser puxado por uma pessoa que a semanas estava falando de você" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        14: {
            "nome_carta": "Bullying Físico | Início | ID: 14",
            "descricao_carta": '"Você vê um de seus colegas colocando o pé na frente de uma menina na intenção de fazê-la cair" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        15: {
            "nome_carta": "Bullying Físico | Início | ID: 15",
            "descricao_carta": '"Ao longe você vê um grupo de pessoas circulando um garoto tampando sua visão do que acontecia" o que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        16: {
            "nome_carta": "Bullying Físico | Início | ID: 16",
            "descricao_carta": '"você tropeça em algo e logo vê que foi uma pessoa que o derrubou" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        17: {
            "nome_carta": "Bullying Físico | Início | ID: 17",
            "descricao_carta": '"Uma menina está sendo encurralada por um grupo de garotos" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        18: {
            "nome_carta": "Bullying Físico | Meio | ID: 18",
            "descricao_carta": "...Você por impulso se defende de quem o atacou... ",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        19: {
            "nome_carta": "Bullying Físico | Meio | ID: 19",
            "descricao_carta": "...Você corre para ajudar a pessoa… ",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        20: {
            "nome_carta": "Bullying Físico | Meio | ID: 20",
            "descricao_carta": "...com medo do que poderia acontecer, você se cala... ",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        21: {
            "nome_carta": "Bullying Físico | Meio | ID: 21",
            "descricao_carta": "...Se calar não irá ajudar, então você busca ajuda de terceiros...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        22: {
            "nome_carta": "Bullying Físico | Meio | ID: 22",
            "descricao_carta": "...Você se intromete na situação com a intenção de acabar com a agressão...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        23: {
            "nome_carta": "Bullying Físico | Meio | ID: 23",
            "descricao_carta": "...Agir sozinho não funcionou, então chamar alguém foi o que lhe restou...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        24: {
            "nome_carta": "Bullying Físico | Meio | ID: 24",
            "descricao_carta": "...Você tenta conversar com os agressores para mudar a situação...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        25: {
            "nome_carta": "Bullying Físico | Final | ID: 25",
            "descricao_carta": "... Sua ação individual foi eficiente! Mas lembre-se de sempre avisar alguém!",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        26: {
            "nome_carta": "Bullying Físico | Final | ID: 26",
            "descricao_carta": "...Você consegue chamar alguém para ajudar e a situação é resolvida.",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        27: {
            "nome_carta": "Bullying Físico | Final | ID: 27",
            "descricao_carta": "...Você tentou agir sozinho mas não deu certo, por sorte alguém mais velho apareceu para lhe ajudar!",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        28: {
            "nome_carta": "Bullying Verbal | Final | ID: 28",
            "descricao_carta": "...Após todas suas ações você conseguiu parar os comentários se afastando das pessoas que o fez.",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        29: {
            "nome_carta": "Bullying Verbal | Final | ID: 29",
            "descricao_carta": "...após debate, as pessoas concordam com você e tudo volta ao normal.",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        30: {
            "nome_carta": "Bullying Verbal | Final | ID: 30",
            "descricao_carta": "...Você conta a um responsável e sua ação resulta em uma chamada de atenção, você conseguiu intervir antes que algo pior acontecesse!",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        31: {
            "nome_carta": "Bullying Moral | Início | ID: 31",
            "descricao_carta": '"Chega ao seus ouvidos boatos sobre você" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        32: {
            "nome_carta": "Bullying Moral | Início | ID: 32",
            "descricao_carta": '"Seus colegas estão espalhando mentiras sobre alguém que não é tão próxima sua" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        33: {
            "nome_carta": "Bullying Moral | Início | ID: 33",
            "descricao_carta": '"seu celular vibra! E ao ligar você vê mensagens sendo espalhadas difamando sua imagem" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        34: {
            "nome_carta": "Bullying Moral | Início | ID: 34",
            "descricao_carta": '"Ao pegar o celular de uma amiga, você vê um grupo no whatsapp criado apenas para comentarem sobre você" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        35: {
            "nome_carta": "Bullying Moral | Início | ID: 35",
            "descricao_carta": '"seu grupo de amigos tenta te incluir na difamação de uma colega" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        36: {
            "nome_carta": "Bullying Moral | Meio | ID: 36",
            "descricao_carta": "...você se desconecta de tudo para evitar ver os comentários...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        37: {
            "nome_carta": "Bullying Moral | Meio | ID: 37",
            "descricao_carta": "...Agir sozinho não ajudou, então você procurou o responsável das pessoas para avisar sobre a situação...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        38: {
            "nome_carta": "Bullying Moral | Meio | ID: 38",
            "descricao_carta": "...Você não se chateou, ao invés disso se afastou e tomou providência para não acontecer com outra pessoa...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        39: {
            "nome_carta": "Bullying Moral | Meio | ID: 39",
            "descricao_carta": "...Você procura ajuda de alguém mais velho já que não soube agir sozinho…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        40: {
            "nome_carta": "Bullying Moral | Meio | ID: 40",
            "descricao_carta": "...Você age rapidamente interceptando a situação e repreende quem está a fazendo…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        41: {
            "nome_carta": "Bullying Moral | Meio | ID: 41",
            "descricao_carta": "...Você se chateia, então decide se afastar deles e avisar algum responsável...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        42: {
            "nome_carta": "Bullying Moral | Meio | ID: 42",
            "descricao_carta": "...Você busca quem começou com os boatos para tomar uma providência…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        43: {
            "nome_carta": "Bullying Psicológico | Início | ID: 43",
            "descricao_carta": '"Ao passar do tempo você se viu sendo excluído pelo seus colegas de atividades que costumava participar" O que você faz',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        44: {
            "nome_carta": "Bullying Psicológico | Início | ID: 44",
            "descricao_carta": '"Você vê um garoto que costumava andar com você intimidando um menino mais novo " O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        45: {
            "nome_carta": "Bullying Psicológico | Início | ID: 45",
            "descricao_carta": '"Durante todo o seu percurso até a sala de aula você observou que um trio de meninos estava perseguindo um que andava sozinho" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        46: {
            "nome_carta": "Bullying Psicológico | Início | ID: 46",
            "descricao_carta": '"Seus amigos começaram a te chantagear com um segredo pessoal seu" O que você faz?',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        47: {
            "nome_carta": "Bullying Psicológico | Início | ID: 47",
            "descricao_carta": '"Você vê um dupla que costumava ser um trio e quem era pra ser a terceira pessoa está sentada sozinha em um dos bancos do ambiente" O que você faz',
            "cor_carta": "azul",
            "tipo_carta": "inicio",
        },
        48: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 48",
            "descricao_carta": "... Você rapidamente vai até a pessoa para tirá-la daquela situação...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        49: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 49",
            "descricao_carta": "...Você busca ajuda de terceiros para parar com a importunação",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        50: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 50",
            "descricao_carta": "...Você vai tentar resolver sozinho! Porém os agressores não gostaram muito...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        51: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 51",
            "descricao_carta": "...ao invés de ajudar a pessoa sozinha você vai atrás dos que estão a excluindo! mas seu esforço foi em vão...",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        52: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 52",
            "descricao_carta": "...Com a atual situação você buscou outros amigos, já que o seus antigos já não eram mais confiáveis…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        53: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 53",
            "descricao_carta": "...Você vai resolver a questão sozinho! E por pouco não deu errado, da próxima vez tente chamar ajuda…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        54: {
            "nome_carta": "Bullying Psicológico | Meio | ID: 54",
            "descricao_carta": "...Você tenta conversar com eles para reverter a situação…",
            "cor_carta": "amarelo",
            "tipo_carta": "meio",
        },
        55: {
            "nome_carta": "Bullying Psicológico | Final | ID: 55",
            "descricao_carta": "...indo ajudar a pessoa sozinha você acaba descobrindo que ela é alguém muito interessante!",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        56: {
            "nome_carta": "Bullying Psicológico | Final | ID: 56",
            "descricao_carta": "... Sua conversa foi efetiva! Mas lembre-se de manter pessoas responsáveis informada sobre o assunto…",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
        57: {
            "nome_carta": "Bullying Psicológico | Final | ID: 57",
            "descricao_carta": "...Sua ação não foi efetiva, porém você conseguiu ajuda antes da situação piorar! Ajuda sempre é bem vinda nesses casos",
            "cor_carta": "roxo",
            "tipo_carta": "final",
        },
    }

    objs = [
        BaralhoCadastro(
            id_carta=key,
            nome_carta=value["nome_carta"],
            tipo_carta=value["tipo_carta"],
            cor_carta=value["cor_carta"],
            descricao_carta=value["descricao_carta"],
        )
        for key, value in info_cards.items()
    ]

    BaralhoCadastro.objects.bulk_create(objs)

    return JsonResponse({"message": "Tabela populada com sucesso!"}, status=201)


def verificar_vitoria_e_notificar():
    """
    Verifica todos os baralhos e cria notificações caso algum jogador
    tenha completado uma sequência válida de cartas (Início, GARIEBL, Fim).
    """
    # Dicionário com todas as histórias fixas
    historias = {
        (1, 6, 29): {
            "tipo": "Bullying Verbal",
            "titulo": "História 1",
            "inicio": "Ao longe, você escuta algumas pessoas rindo e comentando de alguém com um apelido. (Carta 1)",
            "meio": "Você fala com o grupo e tenta argumentar contra essa ação. (Carta 6)",
            "fim": "Após debate, as pessoas concordam com você e tudo volta ao normal. (Carta 29)",
        },
        (2, 9, 28): {
            "tipo": "Bullying Verbal",
            "titulo": "História 2",
            "inicio": "Um colega de sala comenta o peso de outra colega com um tom debochado e humilhante. (Carta 2)",
            "meio": "Você tenta argumentar contra essa ação, mas o grupo não gosta nada de você contrariá-los. (Carta 9)",
            "fim": "Após todas as suas ações, você conseguiu parar os comentários se afastando das pessoas que os fizeram. (Carta 28)",
        },
        (3, 7, 30): {
            "tipo": "Bullying Verbal",
            "titulo": "História 3",
            "inicio": "Enquanto joga futebol, você escuta o time adversário dizendo o quão “perna de pau” você é. (Carta 3)",
            "meio": "Você ignora o comentário, porém cada dia fica pior. (Carta 7)",
            "fim": "Você decide conversar com um responsável, e sua atitude resulta em uma chamada de atenção — você conseguiu intervir antes que algo pior acontecesse. (Carta 30)",
        },
        (4, 11, 29): {
            "tipo": "Bullying Verbal",
            "titulo": "História 4",
            "inicio": "Um trio de meninos chega em você e pergunta qual foi o acidente que fez sua cara ficar “assim” e saem rindo. (Carta 4)",
            "meio": "Após piora,você decide tomar uma providência e conversar com as pessoas (Carta 11)",
            "fim": "Após o debate, as pessoas concordam com você e tudo volta ao normal. (Carta 29)",
        },
        (5, 10, 29): {
            "tipo": "Bullying Verbal",
            "titulo": "História 5",
            "inicio": "Seus amigos comentam sobre a aparência de uma pessoa que você não é tão próxima. (Carta 5)",
            "meio": "após tanto debate sobre o assunto as pessoas acabam concordando com sua argumentação.(Carta 10)",
            "fim": "após o debate as pessoas concordam com você e tudo volta ao normal. (Carta 29)",
        },
        (13, 18, 25): {
            "tipo": "Bullying Físico",
            "titulo": "História 6",
            "inicio": "Você sente seu cabelo ser puxado por alguém que há semanas falava de você. (Carta 13)",
            "meio": "Por impulso, você se defende de quem o atacou. (Carta 18)",
            "fim": "Sua ação individual foi eficiente! Mas lembre-se de sempre avisar alguém. (Carta 25)",
        },
        (14, 22, 26): {
            "tipo": "Bullying Físico",
            "titulo": "História 7",
            "inicio": "Você vê um colega colocando o pé na frente de uma menina para fazê-la cair. (Carta 14)",
            "meio": "Você se intromete na situação com a intenção de acabar com a agressão. (Carta 22)",
            "fim": "Você consegue chamar alguém para ajudar e a situação é resolvida. (Carta 26)",
        },
        (15, 20, 27): {
            "tipo": "Bullying Físico",
            "titulo": "História 8",
            "inicio": "Ao longe, você vê um grupo de pessoas circulando um garoto e tampando sua visão do que acontece. (Carta 15)",
            "meio": "Agir sozinho não funcionou então chamar alguém foi o que lhe restou. (Carta 20)",
            "fim": "Você tentou agir sozinho, mas não deu certo — por sorte alguém mais velho apareceu para ajudar. (Carta 27)",
        },
        (16, 24, 25): {
            "tipo": "Bullying Físico",
            "titulo": "História 9",
            "inicio": "Você tropeça em algo e vê que foi uma pessoa que o derrubou. (Carta 16)",
            "meio": "Você tenta conversar com o agressor para mudar a situação. (Carta 24)",
            "fim": "Sua conversa foi efetiva! Mas lembre-se de avisar alguém. (Carta 25)",
        },
        (17, 19, 25): {
            "tipo": "Bullying Físico",
            "titulo": "História 10",
            "inicio": "Uma menina está sendo encurralada por um grupo de garotos. (Carta 17)",
            "meio": "Você corre para ajudar a pessoa e chama alguém. (Carta 19)",
            "fim": "Você consegue ajuda e a situação é resolvida. (Carta 26)",
        },
        (31, 32, 33): {
            "tipo": "Bullying Moral",
            "titulo": "História 11",
            "inicio": "Chega aos seus ouvidos boatos sobre você. (Carta 31)",
            "meio": "Você busca quem começou com os boatos para tomar uma providência. (Carta 32)",
            "fim": "Com isso, a situação é resolvida e você aprende a importância de não espalhar boatos sobre os outros. (Carta 33)",
        },
        (34, 35, 36): {
            "tipo": "Bullying Moral",
            "titulo": "História 12",
            "inicio": "Seus colegas estão espalhando mentiras sobre alguém. (Carta 34)",
            "meio": "Você age rapidamente e repreende quem está fazendo isso. (Carta 35)",
            "fim": "As pessoas percebem que estavam erradas e param de espalhar mentiras. (Carta 36)",
        },
        (37, 38, 39): {
            "tipo": "Bullying Moral",
            "titulo": "História 13",
            "inicio": "Seu celular vibra e você vê mensagens difamando sua imagem. (Carta 37)",
            "meio": "Você se chateia e decide avisar algum responsável. (Carta 38)",
            "fim": "O responsável intervém e a situação é encerrada. (Carta 39)",
        },
        (40, 41, 42): {
            "tipo": "Bullying Moral",
            "titulo": "História 14",
            "inicio": "Você vê um grupo no WhatsApp criado apenas para falar de você. (Carta 40)",
            "meio": "Você procura ajuda de alguém mais velho já que não soube agir sozinho. (Carta 41)",
            "fim": "Com ajuda, o grupo é desfeito e todos recebem uma orientação sobre respeito. (Carta 42)",
        },
        (43, 44, 45): {
            "tipo": "Bullying Moral",
            "titulo": "História 15",
            "inicio": "Seu grupo tenta te incluir na difamação de uma colega. (Carta 43)",
            "meio": "Você não se chateia, mas se afasta e toma providência para não acontecer de novo. (Carta 44)",
            "fim": "Com seu exemplo, o grupo aprende e evita esse tipo de atitude. (Carta 45)",
        },
        (43, 52, 56): {
            "tipo": "Bullying Psicológico",
            "titulo": "História 16",
            "inicio": "ao passar do tempo você se viu sendo excluída pelo seus colegas de atividade que costumava participar (Carta 43)",
            "meio": "com a atual situação você busca outros amigos já que o seus antigos já não eram mais confiáveis( Carta 52)",
            "fim": "Sua conversa foi efetiva! Mas lembre-se de manter pessoas responsáveis informadas. (Carta 56)",
        },
        (44,48,55): {
            "tipo": "Bullying Psicológico",
            "titulo": "História 17",
            "inicio": "Você vê um garoto que costumava andar com você intimidando um menino mais novo. (Carta 44)",
            "meio": "Você rapidamente vai até a pessoa para tirá-la daquela situação. (Carta 48)",
            "fim": "Indo ajudar sozinho, você acaba descobrindo que ela é alguém muito interessante. (Carta 55)",
        },
        (45, 50, 57): {
            "tipo": "Bullying Psicológico",
            "titulo": "História 18",
            "inicio": "Durante todo seu percurso até a sua sala de aula você observou que um trio de meninos estava perseguindo um que andava sozinho. (Carta 45)",
            "meio": "Você tenta resolver sozinho, mas os agressores não gostaram muito. (Carta 50)",
            "fim": "Sua ação não foi efetiva, mas você conseguiu ajuda antes da situação piorar. (Carta 57)",
        },
        (46, 54, 56): {
            "tipo": "Bullying Psicológico",
            "titulo": "História 19",
            "inicio": "Seus amigos começaram a te chantagear com um segredo pessoal. (Carta 46)",
            "meio": "Você tenta conversar com eles para reverter a situação. (Carta 54)",
            "fim": "Sua conversa foi efetiva! Mas é importante informar alguém responsável. (Carta 56)",
        },
    }

    baralhos = Baralho.objects.all()

    for baralho in baralhos:
        if not (
            baralho.id_carta_inicio and baralho.id_carta_meio and baralho.id_carta_fim
        ):
            continue

        sequencia = (
            baralho.id_carta_inicio,
            baralho.id_carta_meio,
            baralho.id_carta_fim,
        )

        if sequencia in historias:
            historia = historias[sequencia]
            jogador_vencedor = baralho.id_jogador

            # Monta o texto da notificação
            mensagem = (
                f"Jogador {jogador_vencedor.nome_jogador} ganhou o jogo, "
                f"completando as cartas da {historia['titulo']} do {historia['tipo']}:\n\n"
                f"Início: {historia['inicio']}\n"
                f"Meio: {historia['meio']}\n"
                f"Final: {historia['fim']}"
            )

            # Notifica todos os jogadores da mesma partida
            jogadores_partida = Jogador.objects.filter(id_partida=baralho.id_partida)
            for jogador in jogadores_partida:
                Notificacao.objects.create(
                    id_jogador_origem=jogador_vencedor,
                    id_jogador_destino=jogador,
                    id_partida=baralho.id_partida.id_partida,
                    mensagem=mensagem,
                    necessita_atualizar=True,
                    processado=False,
                )


class CriarJogadorView(APIView):
    """
    Cria um jogador vinculado a uma partida.
    Se a partida não for informada, cria uma nova automaticamente.
    """

    @transaction.atomic
    def post(self, request):
        nome_jogador = request.data.get("nome_jogador")
        cor_jogador = request.data.get("cor_jogador")
        id_partida = request.data.get("id_partida")

        if not nome_jogador or not cor_jogador:
            return Response(
                {"error": "Nome e Cor do jogador são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Se não veio id_partida → cria nova partida
        if not id_partida:
            partida = Partida.objects.create()
        else:
            try:
                partida = Partida.objects.get(id_partida=id_partida)
            except Partida.DoesNotExist:
                return Response(
                    {"error": "Partida não encontrada."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Verifica se já existe jogador com a mesma cor nesta partida
        cor_field = f"id_jogador_{cor_jogador.lower()}"
        if hasattr(partida, cor_field) and getattr(partida, cor_field):
            return Response(
                {"error": f"A cor {cor_jogador} já está ocupada nesta partida."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔹 Busca a Casa 1 do Tabuleiro
        try:
            casa_inicial = TabuleiroCadastro.objects.get(numero_casa=1)
        except TabuleiroCadastro.DoesNotExist:
            return Response(
                {"error": "Casa inicial (número 1) não encontrada no tabuleiro."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Cria o jogador já posicionado na casa 1
        jogador = Jogador.objects.create(
            nome_jogador=nome_jogador,
            cor_jogador=cor_jogador,
            id_partida=partida,
            id_casa=casa_inicial.id_casa,  # ✅ começa na Casa 1
        )

        # Atualiza a partida com o jogador na cor correta
        if hasattr(partida, cor_field):
            setattr(partida, cor_field, jogador.id_jogador)
            partida.save()

        # Cria o baralho inicial do jogador
        criar_baralho_para_jogador(jogador, partida)

        ControleJogador.objects.create(
            id_jogador=jogador,
            id_partida=partida,
            sem_jogar_rodadas=0,
            vezes_extra=0,
        )

        return Response(
            {
                "message": "Jogador criado com sucesso!",
                "jogador": {
                    "id_jogador": jogador.id_jogador,
                    "nome_jogador": jogador.nome_jogador,
                    "cor_jogador": jogador.cor_jogador,
                    "id_partida": partida.id_partida,
                    "id_casa": jogador.id_casa,
                },
            },
            status=status.HTTP_201_CREATED,
        )


def criar_baralho_para_jogador(jogador, partida, quantidade=2):
    # Recupera ou cria um baralho para o jogador
    baralho = Baralho.objects.create(
        id_jogador=jogador,
        id_partida=partida,
    )

    # Recupera controle da partida
    controle, _ = ControlePartida.objects.get_or_create(id_partida=partida)

    # Cartas já em circulação (em baralhos de jogadores)
    cartas_em_uso = json.loads(controle.cartas_jogadores or "[]")

    # Cartas já descartadas (caso exista esse controle)
    cartas_descartadas = json.loads(controle.cartas_descartadas or "[]")

    # Todas as cartas do cadastro que podem ser distribuídas (somente inicio e meio)
    cartas_validas = list(
        BaralhoCadastro.objects.filter(tipo_carta__in=["inicio", "meio"]).values_list(
            "id_carta", flat=True
        )
    )

    # Filtra as cartas disponíveis: não podem estar em uso nem descartadas
    cartas_disponiveis = list(
        set(cartas_validas) - set(cartas_em_uso) - set(cartas_descartadas)
    )

    # Se houver menos cartas disponíveis que a quantidade, ajusta para o máximo possível
    if len(cartas_disponiveis) < quantidade:
        quantidade = len(cartas_disponiveis)

    # Se não houver cartas disponíveis, retorna baralho vazio
    if quantidade <= 0:
        baralho.lista_de_cartas = json.dumps([])
        baralho.save()
        return baralho

    # Sorteia as cartas
    cartas_sorteadas = random.sample(cartas_disponiveis, quantidade)

    # Salva as cartas no baralho
    baralho.lista_de_cartas = json.dumps(cartas_sorteadas)
    baralho.save()

    # Atualiza o jogador com o ID do baralho
    jogador.id_baralho = baralho.id_baralho
    jogador.save()

    # Atualiza o controle da partida com as cartas em uso
    controle.cartas_jogadores = json.dumps(cartas_em_uso + cartas_sorteadas)
    controle.save()

    return baralho


class JogadorDetalhesView(APIView):
    """
    Retorna informações detalhadas de um jogador:
    - ID da partida
    - Nome do jogador
    - Cartas do baralho (detalhes vindos de BaralhoCadastro)
    - ID da casa
    - Nome da casa (TabuleiroCadastro)
    """

    def get(self, request, id_jogador):
        try:
            jogador = Jogador.objects.get(id_jogador=id_jogador)
        except Jogador.DoesNotExist:
            return Response(
                {"error": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        # ID da partida
        partida_id = jogador.id_partida.id_partida if jogador.id_partida else None

        # Recupera o baralho
        cartas_detalhes = []
        if jogador.id_baralho:
            try:
                baralho = Baralho.objects.get(id_baralho=jogador.id_baralho)
                lista_ids = json.loads(baralho.lista_de_cartas or "[]")

                # Pega os detalhes das cartas cadastradas
                cartas = BaralhoCadastro.objects.filter(id_carta__in=lista_ids)
                for carta in cartas:
                    cartas_detalhes.append(
                        {
                            "id_carta": carta.id_carta,
                            "nome_carta": carta.nome_carta,
                            "tipo_carta": carta.tipo_carta,
                            "cor_carta": carta.cor_carta,
                            "descricao_carta": carta.descricao_carta,
                        }
                    )

            except Baralho.DoesNotExist:
                cartas_detalhes = []

        # Recupera o nome da casa
        nome_casa = None
        if jogador.id_casa:
            try:
                casa = TabuleiroCadastro.objects.get(id_casa=jogador.id_casa)
                nome_casa = casa.nome_casa
            except TabuleiroCadastro.DoesNotExist:
                nome_casa = None

        # Monta a resposta
        data = {
            "id_partida": partida_id,
            "id_jogador": jogador.id_jogador,
            "nome_jogador": jogador.nome_jogador,
            "cor_jogador": jogador.cor_jogador,
            "id_casa": jogador.id_casa,
            "nome_casa": nome_casa,
            "cartas": cartas_detalhes,
        }

        return Response(data, status=status.HTTP_200_OK)


class CartasJogadorView(APIView):
    """
    Retorna apenas as cartas do jogador a partir do id_jogador.
    """

    def get(self, request, id_jogador):
        try:
            # Verifica se o jogador existe
            jogador = Jogador.objects.get(id_jogador=id_jogador)
        except Jogador.DoesNotExist:
            return Response(
                {"error": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        # Busca o baralho do jogador
        baralho = Baralho.objects.filter(id_jogador=jogador).first()
        if not baralho:
            return Response({"cartas": []}, status=status.HTTP_200_OK)

        # Extrai IDs de cartas da lista
        lista_ids = json.loads(baralho.lista_de_cartas or "[]")

        # Busca detalhes das cartas
        cartas = BaralhoCadastro.objects.filter(id_carta__in=lista_ids).values(
            "id_carta", "nome_carta", "tipo_carta", "cor_carta", "descricao_carta"
        )

        return Response({"cartas": list(cartas)}, status=status.HTTP_200_OK)


class JogadoresPartidaView(APIView):
    """
    Retorna os jogadores de uma partida específica (id_partida)
    """

    def get(self, request, id_partida):
        try:
            partida = Partida.objects.get(id_partida=id_partida)
        except Partida.DoesNotExist:
            return Response(
                {"erro": "Partida não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )

        # Busca jogadores ativos vinculados à partida
        jogadores = Jogador.objects.filter(id_partida=partida).values(
            "id_jogador", "nome_jogador"
        )

        return Response({"jogadores": list(jogadores)}, status=status.HTTP_200_OK)


class PopularTabuleiroView(View):
    def get(self, request):
        # 🔹 Se já houver dados no tabuleiro ou ações, não popula de novo
        if AcaoCadastro.objects.exists() or TabuleiroCadastro.objects.exists():
            return JsonResponse(
                {"status": "Ops!", "msg": "O tabuleiro já foi populado anteriormente."},
                status=400,
            )

        # 1. Ações únicas
        acoes = [
            ("Início", None, "Casa inicial do jogo"),
            ("Ganhar carta FIM", "FIM", "Jogador ganha uma carta do tipo FIM"),
            ("Ganhar carta MEIO", "MEIO", "Jogador ganha uma carta do tipo MEIO"),
            ("Ganhar carta INICIO", "INICIO", "Jogador ganha uma carta do tipo INÍCIO"),
            (
                "Ganhar carta INICIO-MEIO-FIM",
                None,
                "Jogador ganha uma carta de cada tipo",
            ),
            (
                "Troca cartas frente",
                None,
                "Troque todas as cartas com o jogador à frente",
            ),
            (
                "Troca cartas direita",
                None,
                "Troque todas as cartas com o jogador à direita",
            ),
            (
                "Troca cartas esquerda",
                None,
                "Troque todas as cartas com o jogador à esquerda",
            ),
            ("Doe vez ou perca carta", None, "Doe a vez a alguém ou perca uma carta"),
            ("Doe 1 carta", None, "Doe uma carta a alguém de sua escolha"),
            ("Doe vez", None, "Doe a vez a alguém de sua escolha"),
            ("Desafio elogio", None, "Elogie alguém ou perca uma carta"),
            ("Roubar carta esquerda", None, "Roube uma carta do jogador à esquerda"),
            ("Roubar carta direita", None, "Roube uma carta do jogador à direita"),
            ("Roubar carta qualquer", None, "Roube uma carta de qualquer jogador"),
            (
                "Entregar carta frente",
                None,
                "Pegue uma carta sem ver e entregue ao jogador à frente",
            ),
            (
                "Entregar carta próximo",
                None,
                "Pegue uma carta sem ver e entregue ao próximo jogador",
            ),
            (
                "Ver baralho esquerda",
                None,
                "Veja o baralho da esquerda e troque 1 carta",
            ),
            ("Ver baralho direita", None, "Veja o baralho da direita e troque 1 carta"),
            ("Avançar casas", None, "Avance 2 casas"),
            ("Voltar casas", None, "Volte 2 casas"),
            (
                "Voltar início + carta FIM",
                "FIM",
                "Volte ao início e ganhe uma carta FIM",
            ),
            ("Perder carta MEIO", "MEIO", "Perde uma carta MEIO"),
            ("Perder carta INICIO", "INICIO", "Perde uma carta INÍCIO"),
            ("Perder carta FINAL", "FIM", "Perde uma carta FINAL"),
            (
                "Perder carta FINAL condicional",
                "FIM",
                "Perde sua carta FINAL se não perdeu a vez",
            ),
            ("Perder vez", None, "Jogador perde sua vez"),
            ("Perder rodadas", None, "Jogador fica 2 rodadas sem jogar"),
            ("Jogue novamente", None, "Jogue novamente"),
        ]

        acao_objs = {}
        for nome, tipo, desc in acoes:
            obj = AcaoCadastro.objects.create(
                nome_acao=nome,
                tipo_carta=tipo,
                descricao=desc,
            )
            acao_objs[nome] = obj

        # 2. Casas mapeadas
        casas = [
            (1, "Início", "Início"),
            (2, "Ganhe 1 carta de FIM", "Ganhar carta FIM"),
            (3, "Sorte! Jogue novamente", "Jogue novamente"),
            (4, "Troque suas cartas com o jogador à frente", "Troca cartas frente"),
            (5, "Doe a sua vez a alguém ou perca 1 carta", "Doe vez ou perca carta"),
            (6, "Sorte! Ganhe 1 carta de MEIO", "Ganhar carta MEIO"),
            (7, "Avance 2 casas", "Avançar casas"),
            (8, "Sorte! Ganhe uma carta de MEIO", "Ganhar carta MEIO"),
            (9, "Troque suas cartas com o jogador à direita", "Troca cartas direita"),
            (10, "Volte 2 casas", "Voltar casas"),
            (11, "Roube 1 carta do jogador à esquerda", "Roubar carta esquerda"),
            (12, "Azar! Perca uma carta de MEIO", "Perder carta MEIO"),
            (13, "Sorte! Jogue novamente", "Jogue novamente"),
            (14, "Doe 1 carta a alguém de sua escolha", "Doe 1 carta"),
            (15, "Roube 1 carta de um jogador", "Roubar carta qualquer"),
            (
                16,
                "Volte ao início e pegue uma carta de FINAL",
                "Voltar início + carta FIM",
            ),
            (
                17,
                "Veja o baralho do jogador à esquerda e troque 1 carta",
                "Ver baralho esquerda",
            ),
            (18, "Fique 2 rodadas sem jogar", "Perder rodadas"),
            (
                19,
                "Sorte! Pegue 1 carta de INÍCIO, MEIO e FIM",
                "Ganhar carta INICIO-MEIO-FIM",
            ),
            (
                20,
                "Pegue 1 carta sem ver e entregue para o jogador à frente",
                "Entregar carta frente",
            ),
            (21, "Desafio! Elogie alguém ou perca 1 carta", "Desafio elogio"),
            (22, "Troque suas cartas com o jogador à frente", "Troca cartas frente"),
            (23, "Sorte! Pegue 1 carta de início", "Ganhar carta INICIO"),
            (24, "Doe sua vez a alguém de sua escolha", "Doe vez"),
            (
                25,
                "Pegue 1 carta sem ver e entregue para o próximo jogador",
                "Entregar carta próximo",
            ),
            (26, "Sorte! Pegue 1 carta inicial", "Ganhar carta INICIO"),
            (27, "Desafio! Elogie alguém ou perca 1 carta", "Desafio elogio"),
            (
                28,
                "Veja o baralho do jogador à direita e troque 1 carta",
                "Ver baralho direita",
            ),
            (29, "Roube 1 carta do jogador à direita", "Roubar carta direita"),
            (30, "Azar! Perca 1 carta de INÍCIO", "Perder carta INICIO"),
            (31, "Perca sua vez!", "Perder vez"),
            (32, "Volte 2 casas", "Voltar casas"),
            (33, "Ganhe 1 carta final", "Ganhar carta FIM"),
            (
                34,
                "Troque suas cartas com o jogador da sua esquerda",
                "Troca cartas esquerda",
            ),
            (
                35,
                "Perca sua carta FINAL caso não tenha perdido a sua vez",
                "Perder carta FINAL condicional",
            ),
            (36, "Azar! Perca uma carta FINAL", "Perder carta FINAL"),
        ]

        for numero, nome, acao_nome in casas:
            TabuleiroCadastro.objects.create(
                numero_casa=numero,
                nome_casa=nome,
                acao=acao_objs[acao_nome],
            )

        return JsonResponse(
            {"status": "Finalizado!", "msg": "Tabuleiro populado com sucesso"}
        )


class RolarDadoView(APIView):
    """
    Move o jogador no tabuleiro conforme o valor do dado.
    Retorna também o id_acao da casa para facilitar lógica no cliente.
    """

    @transaction.atomic
    def post(self, request):
        try:
            valor_dado = int(request.data.get("valor_dado", 0))
            id_jogador = request.data.get("id_jogador")

            if not id_jogador or valor_dado not in range(1, 7):
                return Response(
                    {
                        "error": "Parâmetros inválidos. Informe id_jogador e valor_dado (1-6)."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            jogador = Jogador.objects.get(id_jogador=id_jogador)

            ultima_casa = TabuleiroCadastro.objects.order_by("-numero_casa").first()
            if not ultima_casa:
                return Response(
                    {"error": "Tabuleiro não está populado."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            posicao_atual = jogador.id_casa or 1
            nova_posicao = posicao_atual + valor_dado

            if nova_posicao > ultima_casa.numero_casa:
                excedente = nova_posicao - ultima_casa.numero_casa
                nova_posicao = excedente if excedente > 0 else 1

            jogador.id_casa = nova_posicao
            jogador.save()

            casa = TabuleiroCadastro.objects.get(numero_casa=nova_posicao)

            # Inclui id_acao no retorno
            return Response(
                {
                    "message": f"Jogador {jogador.nome_jogador} moveu {valor_dado} casas.",
                    "nova_posicao": {
                        "id_casa": jogador.id_casa,
                        "nome_casa": casa.nome_casa,
                        "id_acao": casa.acao.id_acao,  # <-- aqui está o id_acao
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Jogador.DoesNotExist:
            return Response(
                {"error": "Jogador não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET"])
def jogador_esquerda(request, id_jogador):
    try:
        jogador = Jogador.objects.get(id_jogador=id_jogador)
        jogador_esquerda_id = get_jogador_esquerda(jogador)
        if not jogador_esquerda_id:
            return Response({"mensagem": "Não há jogador à esquerda."}, status=404)

        jogador_esquerda = Jogador.objects.get(id_jogador=jogador_esquerda_id)

        return Response(
            {
                "id_jogador_esquerda": int(jogador_esquerda.id_jogador),
                "nome_jogador_esquerda": jogador_esquerda.nome_jogador,
            },
            status=200,
        )

    except Jogador.DoesNotExist:
        return Response({"erro": "Jogador não encontrado."}, status=404)


@api_view(["GET"])
def jogador_direita(request, id_jogador):
    try:
        jogador = Jogador.objects.get(id_jogador=id_jogador)
        jogador_direita_id = get_jogador_direita(jogador)
        if not jogador_direita_id:
            return Response({"mensagem": "Não há jogador à direita."}, status=404)

        jogador_direita = Jogador.objects.get(id_jogador=jogador_direita_id)

        return Response(
            {
                "id_jogador_direita": int(jogador_direita.id_jogador),
                "nome_jogador_direita": jogador_direita.nome_jogador,
            },
            status=200,
        )

    except Jogador.DoesNotExist:
        return Response({"erro": "Jogador não encontrado."}, status=404)


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================


def get_jogador_esquerda(jogador):
    """
    Retorna o id_jogador do jogador imediatamente à esquerda.
    """
    partida = jogador.id_partida
    if not partida:
        return None

    ordem_cores = ["amarelo", "azul", "preto", "roxo"]

    cor_atual = jogador.cor_jogador.lower()
    if cor_atual not in ordem_cores:
        return None

    idx_atual = ordem_cores.index(cor_atual)
    prox_idx = (idx_atual - 1) % len(ordem_cores)

    tentativas = 0
    while tentativas < len(ordem_cores):
        cor_prox = ordem_cores[prox_idx]
        jogador_id = getattr(partida, f"id_jogador_{cor_prox}", None)
        if jogador_id:
            return jogador_id
        prox_idx = (prox_idx - 1) % len(ordem_cores)
        tentativas += 1

    return None


def get_jogador_direita(jogador):
    """
    Retorna o id_jogador do jogador imediatamente à direita.
    """
    partida = jogador.id_partida
    if not partida:
        return None

    ordem_cores = ["amarelo", "azul", "preto", "roxo"]

    cor_atual = jogador.cor_jogador.lower()
    if cor_atual not in ordem_cores:
        return None

    idx_atual = ordem_cores.index(cor_atual)
    prox_idx = (idx_atual + 1) % len(ordem_cores)

    tentativas = 0
    while tentativas < len(ordem_cores):
        cor_prox = ordem_cores[prox_idx]
        jogador_id = getattr(partida, f"id_jogador_{cor_prox}", None)
        if jogador_id:
            return jogador_id
        prox_idx = (prox_idx + 1) % len(ordem_cores)
        tentativas += 1

    return None


def perder_carta(jogador, casa, acao):
    """Executa a lógica de remover carta do jogador."""
    baralho = Baralho.objects.filter(
        id_jogador=jogador, id_partida=jogador.id_partida
    ).first()

    if not baralho or not baralho.lista_de_cartas:
        return {
            "cartas_removidas": [],
            "mensagem": f"Jogador {jogador.nome_jogador} não possui cartas.",
        }

    lista_cartas_jogador = json.loads(baralho.lista_de_cartas)

    # Define tipo de carta a ser perdida
    tipo_perdido = {23: "meio", 24: "inicio", 25: "final"}.get(acao.id_acao)

    carta_removida = None
    for id_carta in lista_cartas_jogador:
        carta = BaralhoCadastro.objects.get(id_carta=id_carta)
        if carta.tipo_carta.upper() == tipo_perdido.upper():
            carta_removida = carta
            lista_cartas_jogador.remove(id_carta)
            break

    if not carta_removida:
        return {
            "cartas_removidas": [],
            "mensagem": f"Nenhuma carta do tipo {tipo_perdido} encontrada no baralho do jogador.",
        }

    # Atualiza baralho do jogador
    baralho.lista_de_cartas = json.dumps(lista_cartas_jogador)
    baralho.save()

    # Atualiza controle global
    controle = ControlePartida.objects.filter(id_partida=jogador.id_partida).first()
    if controle:
        cartas_jogadores = (
            json.loads(controle.cartas_jogadores) if controle.cartas_jogadores else []
        )
        if carta_removida.id_carta in cartas_jogadores:
            cartas_jogadores.remove(carta_removida.id_carta)
        controle.cartas_jogadores = json.dumps(cartas_jogadores)

        descartadas = (
            json.loads(controle.cartas_descartadas)
            if controle.cartas_descartadas
            else []
        )
        descartadas.append(carta_removida.id_carta)
        controle.cartas_descartadas = json.dumps(descartadas)

        controle.save()

    return {
        "cartas_removidas": [
            {
                "id_carta": carta_removida.id_carta,
                "nome": carta_removida.nome_carta,
                "tipo": carta_removida.tipo_carta,
            }
        ]
    }


@csrf_exempt
def descartar_carta_por_id(request, id_jogador, id_carta):
    """Descarta uma carta específica escolhida pelo jogador."""

    # Recupera jogador
    jogador = Jogador.objects.filter(id_jogador=id_jogador).first()
    if not jogador:
        return JsonResponse(
            {"mensagem": f"Jogador com id {id_jogador} não encontrado."},
            status=404,
        )

    # Recupera baralho do jogador
    baralho = Baralho.objects.filter(
        id_jogador=jogador, id_partida=jogador.id_partida
    ).first()

    if not baralho or not baralho.lista_de_cartas:
        return JsonResponse(
            {
                "cartas_removidas": [],
                "mensagem": f"Jogador {jogador.nome_jogador} não possui cartas.",
            }
        )

    lista_cartas_jogador = json.loads(baralho.lista_de_cartas)

    # Verifica se a carta está no baralho do jogador
    if id_carta not in lista_cartas_jogador:
        return JsonResponse(
            {
                "cartas_removidas": [],
                "mensagem": f"A carta {id_carta} não está no baralho do jogador {jogador.nome_jogador}.",
            }
        )

    # Remove carta do baralho do jogador
    lista_cartas_jogador.remove(id_carta)
    baralho.lista_de_cartas = json.dumps(lista_cartas_jogador)
    baralho.save()

    # Recupera informações da carta removida
    carta_removida = BaralhoCadastro.objects.get(id_carta=id_carta)

    # Atualiza controle global
    controle = ControlePartida.objects.filter(id_partida=jogador.id_partida).first()
    if controle:
        cartas_jogadores = (
            json.loads(controle.cartas_jogadores) if controle.cartas_jogadores else []
        )
        if id_carta in cartas_jogadores:
            cartas_jogadores.remove(id_carta)
        controle.cartas_jogadores = json.dumps(cartas_jogadores)

        descartadas = (
            json.loads(controle.cartas_descartadas)
            if controle.cartas_descartadas
            else []
        )
        descartadas.append(id_carta)
        controle.cartas_descartadas = json.dumps(descartadas)

        controle.save()

    return JsonResponse(
        {
            "cartas_removidas": [
                {
                    "id_carta": carta_removida.id_carta,
                    "nome": carta_removida.nome_carta,
                    "tipo": carta_removida.tipo_carta,
                }
            ],
            "mensagem": f"Carta {carta_removida.nome_carta} descartada com sucesso.",
        }
    )


def ganhar_carta(jogador, casa, acao, tipo_carta=None):
    """Executa a lógica de adicionar carta ao jogador."""
    controle = ControlePartida.objects.filter(id_partida=jogador.id_partida).first()
    if not controle:
        raise Exception("Controle da partida não encontrado.")

    entregues_ids = []
    if controle.cartas_jogadores:
        entregues_ids += json.loads(controle.cartas_jogadores)
    if controle.cartas_descartadas:
        entregues_ids += json.loads(controle.cartas_descartadas)

    baralho, _ = Baralho.objects.get_or_create(
        id_jogador=jogador, id_partida=jogador.id_partida
    )
    lista_cartas_jogador = (
        json.loads(baralho.lista_de_cartas) if baralho.lista_de_cartas else []
    )

    cartas_adicionadas = []

    def buscar_carta_disponivel(tipo):
        todas_cartas = BaralhoCadastro.objects.filter(tipo_carta__iexact=tipo)
        for c in todas_cartas:
            if c.id_carta not in entregues_ids:
                entregues_ids.append(c.id_carta)
                return c
        return None

    # Regras normais (ações 2,3,4)
    if acao.id_acao in [2, 3, 4]:
        tipos_a_distribuir = {
            2: ["final"],
            3: ["meio"],
            4: ["inicio"],
        }[acao.id_acao]

        for tipo in tipos_a_distribuir:
            carta = buscar_carta_disponivel(tipo)
            if carta:
                lista_cartas_jogador.append(carta.id_carta)
                cartas_adicionadas.append(carta)

    # Regra especial (ação 5)
    elif acao.id_acao == 5:
        if not tipo_carta or tipo_carta.lower() not in ["inicio", "meio", "final"]:
            raise Exception(
                "É necessário informar um tipo de carta válido: 'inicio', 'meio' ou 'final'."
            )

        carta = buscar_carta_disponivel(tipo_carta.lower())
        if carta:
            lista_cartas_jogador.append(carta.id_carta)
            cartas_adicionadas.append(carta)

    baralho.lista_de_cartas = json.dumps(lista_cartas_jogador)
    baralho.save()

    controle.cartas_jogadores = json.dumps(entregues_ids)
    controle.save()

    return {
        "cartas_adicionadas": [
            {
                "id_carta": c.id_carta,
                "nome": c.nome_carta,
                "tipo": c.tipo_carta,
            }
            for c in cartas_adicionadas
        ]
    }


def trocar_com_jogador_frente(jogador, casa, acao):
    """
    Troca todas as cartas do jogador atual com outro jogador, seguindo regras:
      - Se só houver 1 jogador na partida → não faz nada
      - Se houver apenas 2 jogadores → troca com o outro
      - Se houver 3 ou mais jogadores → troca com o segundo próximo válido (não o imediato)
    """
    partida = jogador.id_partida
    if not partida:
        return {"mensagem": "Jogador não está vinculado a uma partida."}

    ordem_cores = ["amarelo", "azul", "preto", "roxo"]
    cor_atual = jogador.cor_jogador.lower()
    if cor_atual not in ordem_cores:
        return {"mensagem": f"A cor {cor_atual} não é válida para troca."}

    idx_atual = ordem_cores.index(cor_atual)

    jogadores_ids = {
        "amarelo": partida.id_jogador_amarelo,
        "azul": partida.id_jogador_azul,
        "preto": partida.id_jogador_preto,
        "roxo": partida.id_jogador_roxo,
    }
    jogadores_ativos = [cor for cor, jid in jogadores_ids.items() if jid]

    if len(jogadores_ativos) <= 1:
        return {"mensagem": "Não há outros jogadores para realizar a troca."}

    passos = 1 if len(jogadores_ativos) == 2 else 2

    prox_idx = idx_atual
    jogador_destino_id = None
    tentativas, encontrados = 0, 0
    while tentativas < len(ordem_cores) * 2:
        prox_idx = (prox_idx + 1) % len(ordem_cores)
        cor_prox = ordem_cores[prox_idx]
        jogador_id = jogadores_ids.get(cor_prox)
        if jogador_id:
            encontrados += 1
            if encontrados == passos:
                jogador_destino_id = jogador_id
                break
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Nenhum jogador válido encontrado para troca."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)

    baralho_origem, _ = Baralho.objects.get_or_create(
        id_jogador=jogador, id_partida=partida
    )
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=partida
    )

    cartas_origem = json.loads(baralho_origem.lista_de_cartas or "[]")
    cartas_destino = json.loads(baralho_destino.lista_de_cartas or "[]")

    baralho_origem.lista_de_cartas = json.dumps(cartas_destino)
    baralho_destino.lista_de_cartas = json.dumps(cartas_origem)
    baralho_origem.save()
    baralho_destino.save()

    # Cria notificações para ambos
    criar_notificacao(
        jogador, jogador_destino, "Seu baralho foi trocado com outro jogador."
    )

    return {
        "mensagem": f"Cartas trocadas entre {jogador.nome_jogador} e {jogador_destino.nome_jogador}.",
        "jogador_origem": {
            "id": jogador.id_jogador,
            "nome": jogador.nome_jogador,
            "cartas_finais": cartas_destino,
        },
        "jogador_destino": {
            "id": jogador_destino.id_jogador,
            "nome": jogador_destino.nome_jogador,
            "cartas_finais": cartas_origem,
        },
    }


def trocar_com_jogador_direita(jogador, casa, acao):
    """
    Troca todas as cartas do jogador atual com o jogador à direita.
    """
    partida = jogador.id_partida
    if not partida:
        return {"mensagem": "Jogador não está vinculado a uma partida."}

    ordem_cores = ["amarelo", "azul", "preto", "roxo"]
    cor_atual = jogador.cor_jogador.lower()
    if cor_atual not in ordem_cores:
        return {"mensagem": f"A cor {cor_atual} não é válida para troca."}

    idx_atual = ordem_cores.index(cor_atual)
    jogadores_ids = [
        partida.id_jogador_amarelo,
        partida.id_jogador_azul,
        partida.id_jogador_preto,
        partida.id_jogador_roxo,
    ]
    jogadores_ativos = [j for j in jogadores_ids if j]

    if len(jogadores_ativos) <= 1:
        return {"mensagem": "Não há outros jogadores para realizar a troca."}

    prox_idx, jogador_destino_id, tentativas = (
        (idx_atual + 1) % len(ordem_cores),
        None,
        0,
    )
    while tentativas < len(ordem_cores):
        cor_prox = ordem_cores[prox_idx]
        jogador_destino_id = getattr(partida, f"id_jogador_{cor_prox}", None)
        if jogador_destino_id:
            break
        prox_idx = (prox_idx + 1) % len(ordem_cores)
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Nenhum jogador válido encontrado para troca."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)
    baralho_origem, _ = Baralho.objects.get_or_create(
        id_jogador=jogador, id_partida=partida
    )
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=partida
    )

    cartas_origem = json.loads(baralho_origem.lista_de_cartas or "[]")
    cartas_destino = json.loads(baralho_destino.lista_de_cartas or "[]")

    baralho_origem.lista_de_cartas = json.dumps(cartas_destino)
    baralho_destino.lista_de_cartas = json.dumps(cartas_origem)
    baralho_origem.save()
    baralho_destino.save()

    criar_notificacao(
        jogador, jogador_destino, "Seu baralho foi trocado com o jogador à direita."
    )

    return {
        "mensagem": f"Cartas trocadas entre {jogador.nome_jogador} e {jogador_destino.nome_jogador}.",
        "jogador_origem": {
            "id": jogador.id_jogador,
            "nome": jogador.nome_jogador,
            "cartas_finais": cartas_destino,
        },
        "jogador_destino": {
            "id": jogador_destino.id_jogador,
            "nome": jogador_destino.nome_jogador,
            "cartas_finais": cartas_origem,
        },
    }


def trocar_com_jogador_esquerda(jogador, casa, acao):
    """
    Troca todas as cartas do jogador atual com o jogador à esquerda.
    """
    partida = jogador.id_partida
    if not partida:
        return {"mensagem": "Jogador não está vinculado a uma partida."}

    ordem_cores = ["amarelo", "azul", "preto", "roxo"]
    cor_atual = jogador.cor_jogador.lower()
    if cor_atual not in ordem_cores:
        return {"mensagem": f"A cor {cor_atual} não é válida para troca."}

    idx_atual = ordem_cores.index(cor_atual)
    jogadores_ids = [
        partida.id_jogador_amarelo,
        partida.id_jogador_azul,
        partida.id_jogador_preto,
        partida.id_jogador_roxo,
    ]
    jogadores_ativos = [j for j in jogadores_ids if j]

    if len(jogadores_ativos) <= 1:
        return {"mensagem": "Não há outros jogadores para realizar a troca."}

    prox_idx, jogador_destino_id, tentativas = (
        (idx_atual - 1) % len(ordem_cores),
        None,
        0,
    )
    while tentativas < len(ordem_cores):
        cor_prox = ordem_cores[prox_idx]
        jogador_destino_id = getattr(partida, f"id_jogador_{cor_prox}", None)
        if jogador_destino_id:
            break
        prox_idx = (prox_idx - 1) % len(ordem_cores)
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Nenhum jogador válido encontrado para troca."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)
    baralho_origem, _ = Baralho.objects.get_or_create(
        id_jogador=jogador, id_partida=partida
    )
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=partida
    )

    cartas_origem = json.loads(baralho_origem.lista_de_cartas or "[]")
    cartas_destino = json.loads(baralho_destino.lista_de_cartas or "[]")

    baralho_origem.lista_de_cartas = json.dumps(cartas_destino)
    baralho_destino.lista_de_cartas = json.dumps(cartas_origem)
    baralho_origem.save()
    baralho_destino.save()

    criar_notificacao(
        jogador, jogador_destino, "Seu baralho foi trocado com o jogador à esquerda."
    )

    return {
        "mensagem": f"Cartas trocadas entre {jogador.nome_jogador} e {jogador_destino.nome_jogador}.",
        "jogador_origem": {
            "id": jogador.id_jogador,
            "nome": jogador.nome_jogador,
            "cartas_finais": cartas_destino,
        },
        "jogador_destino": {
            "id": jogador_destino.id_jogador,
            "nome": jogador_destino.nome_jogador,
            "cartas_finais": cartas_origem,
        },
    }


def trocar_carta_com_esquerda(jogador, id_carta_jogador, id_carta_esquerda):
    """
    Troca uma carta do jogador atual com uma carta do jogador à esquerda.
    - O jogador é identificado pelo objeto `Jogador` passado.
    - São trocadas apenas as cartas informadas no body da requisição.
    """

    try:
        partida = jogador.id_partida
        if not partida:
            return {"mensagem": "Jogador não está vinculado a uma partida."}

        # Define a ordem das cores
        ordem_cores = ["amarelo", "azul", "preto", "roxo"]
        cor_atual = jogador.cor_jogador.lower()

        if cor_atual not in ordem_cores:
            return {"mensagem": f"A cor {cor_atual} não é válida para troca."}

        idx_atual = ordem_cores.index(cor_atual)

        # Busca o jogador válido à esquerda (anti-horário)
        prox_idx, jogador_esquerda_id, tentativas = (
            (idx_atual - 1) % len(ordem_cores),
            None,
            0,
        )
        while tentativas < len(ordem_cores):
            cor_prox = ordem_cores[prox_idx]
            jogador_esquerda_id = getattr(partida, f"id_jogador_{cor_prox}", None)
            if jogador_esquerda_id:
                break
            prox_idx = (prox_idx - 1) % len(ordem_cores)
            tentativas += 1

        if not jogador_esquerda_id:
            return {"mensagem": "Não há jogador à esquerda válido."}

        jogador_esquerda = Jogador.objects.get(id_jogador=jogador_esquerda_id)

        # Recupera baralhos
        baralho_jogador, _ = Baralho.objects.get_or_create(
            id_jogador=jogador, id_partida=partida
        )
        baralho_esquerda, _ = Baralho.objects.get_or_create(
            id_jogador=jogador_esquerda, id_partida=partida
        )

        cartas_jogador = json.loads(baralho_jogador.lista_de_cartas or "[]")
        cartas_esquerda = json.loads(baralho_esquerda.lista_de_cartas or "[]")

        # Valida se as cartas estão nos baralhos corretos
        if int(id_carta_jogador) not in cartas_jogador:
            return {
                "erro": f"A carta {id_carta_jogador} não está no baralho do jogador {jogador.nome_jogador}."
            }
        if int(id_carta_esquerda) not in cartas_esquerda:
            return {
                "erro": f"A carta {id_carta_esquerda} não está no baralho do jogador {jogador_esquerda.nome_jogador}."
            }

        # Faz a troca
        cartas_jogador.remove(int(id_carta_jogador))
        cartas_esquerda.remove(int(id_carta_esquerda))
        cartas_jogador.append(int(id_carta_esquerda))
        cartas_esquerda.append(int(id_carta_jogador))

        # Salva nos baralhos
        baralho_jogador.lista_de_cartas = json.dumps(cartas_jogador)
        baralho_esquerda.lista_de_cartas = json.dumps(cartas_esquerda)
        baralho_jogador.save()
        baralho_esquerda.save()

        # Busca os nomes das cartas trocadas
        carta_jogador_nome = BaralhoCadastro.objects.get(
            id_carta=id_carta_jogador
        ).nome_carta
        carta_esquerda_nome = BaralhoCadastro.objects.get(
            id_carta=id_carta_esquerda
        ).nome_carta

        # Cria notificação detalhada
        criar_notificacao(
            jogador,
            jogador_esquerda,
            f"Troca de carta entre jogadores! {jogador.nome_jogador} trocou a carta '{carta_jogador_nome}' dele, "
            f"pela sua carta '{carta_esquerda_nome}'.",
        )

        # Prepara retorno detalhado
        cartas_origem = list(
            BaralhoCadastro.objects.filter(id_carta__in=cartas_jogador).values(
                "id_carta", "nome_carta"
            )
        )
        cartas_destino = list(
            BaralhoCadastro.objects.filter(id_carta__in=cartas_esquerda).values(
                "id_carta", "nome_carta"
            )
        )

        return {
            "mensagem": f"Cartas trocadas entre {jogador.nome_jogador} e {jogador_esquerda.nome_jogador}.",
            "jogador_origem": {
                "id": jogador.id_jogador,
                "nome": jogador.nome_jogador,
                "cartas_finais": cartas_origem,
            },
            "jogador_destino": {
                "id": jogador_esquerda.id_jogador,
                "nome": jogador_esquerda.nome_jogador,
                "cartas_finais": cartas_destino,
            },
        }

    except Exception as e:
        print("=" * 80)
        print("ERRO AO TROCAR CARTAS ENTRE JOGADORES")
        print(f"Jogador origem: {getattr(jogador, 'nome_jogador', '?')}")
        print(f"id_carta_jogador: {id_carta_jogador}")
        print(f"id_carta_esquerda: {id_carta_esquerda}")
        print("Traceback:")
        traceback.print_exc()
        print("=" * 80)
        return JsonResponse(
            {
                "erro": "Erro interno ao processar a troca de cartas.",
                "detalhes": str(e),
                "traceback": traceback.format_exc(),
            },
            status=400,
        )


def trocar_carta_com_direita(jogador, id_carta_jogador, id_carta_direita):
    """
    Troca uma carta do jogador atual com uma carta do jogador à direita.
    - O jogador é identificado pelo objeto `Jogador` passado.
    - São trocadas apenas as cartas informadas no body da requisição.
    """

    try:
        partida = jogador.id_partida
        if not partida:
            return {"mensagem": "Jogador não está vinculado a uma partida."}

        # Define a ordem das cores
        ordem_cores = ["amarelo", "azul", "preto", "roxo"]
        cor_atual = jogador.cor_jogador.lower()

        if cor_atual not in ordem_cores:
            return {"mensagem": f"A cor {cor_atual} não é válida para troca."}

        idx_atual = ordem_cores.index(cor_atual)

        # Busca o jogador válido à direita (sentido horário)
        prox_idx, jogador_direita_id, tentativas = (
            (idx_atual + 1) % len(ordem_cores),
            None,
            0,
        )
        while tentativas < len(ordem_cores):
            cor_prox = ordem_cores[prox_idx]
            jogador_direita_id = getattr(partida, f"id_jogador_{cor_prox}", None)
            if jogador_direita_id:
                break
            prox_idx = (prox_idx + 1) % len(ordem_cores)
            tentativas += 1

        if not jogador_direita_id:
            return {"mensagem": "Não há jogador à direita válido."}

        jogador_direita = Jogador.objects.get(id_jogador=jogador_direita_id)

        # Recupera baralhos
        baralho_jogador, _ = Baralho.objects.get_or_create(
            id_jogador=jogador, id_partida=partida
        )
        baralho_direita, _ = Baralho.objects.get_or_create(
            id_jogador=jogador_direita, id_partida=partida
        )

        cartas_jogador = json.loads(baralho_jogador.lista_de_cartas or "[]")
        cartas_direita = json.loads(baralho_direita.lista_de_cartas or "[]")

        # Valida se as cartas estão nos baralhos corretos
        if int(id_carta_jogador) not in cartas_jogador:
            return {
                "erro": f"A carta {id_carta_jogador} não está no baralho do jogador {jogador.nome_jogador}."
            }
        if int(id_carta_direita) not in cartas_direita:
            return {
                "erro": f"A carta {id_carta_direita} não está no baralho do jogador {jogador_direita.nome_jogador}."
            }

        # Faz a troca
        cartas_jogador.remove(int(id_carta_jogador))
        cartas_direita.remove(int(id_carta_direita))
        cartas_jogador.append(int(id_carta_direita))
        cartas_direita.append(int(id_carta_jogador))

        # Salva nos baralhos
        baralho_jogador.lista_de_cartas = json.dumps(cartas_jogador)
        baralho_direita.lista_de_cartas = json.dumps(cartas_direita)
        baralho_jogador.save()
        baralho_direita.save()

        # Busca os nomes das cartas trocadas
        carta_jogador_nome = BaralhoCadastro.objects.get(
            id_carta=id_carta_jogador
        ).nome_carta
        carta_direita_nome = BaralhoCadastro.objects.get(
            id_carta=id_carta_direita
        ).nome_carta

        # Cria notificação detalhada
        criar_notificacao(
            jogador,
            jogador_direita,
            f"Troca de carta entre jogadores! {jogador.nome_jogador} trocou a carta '{carta_jogador_nome}' dele, "
            f"pela sua carta '{carta_direita_nome}'.",
        )

        # Prepara retorno detalhado
        cartas_origem = list(
            BaralhoCadastro.objects.filter(id_carta__in=cartas_jogador).values(
                "id_carta", "nome_carta"
            )
        )
        cartas_destino = list(
            BaralhoCadastro.objects.filter(id_carta__in=cartas_direita).values(
                "id_carta", "nome_carta"
            )
        )

        return {
            "mensagem": f"Cartas trocadas entre {jogador.nome_jogador} e {jogador_direita.nome_jogador}.",
            "jogador_origem": {
                "id": jogador.id_jogador,
                "nome": jogador.nome_jogador,
                "cartas_finais": cartas_origem,
            },
            "jogador_destino": {
                "id": jogador_direita.id_jogador,
                "nome": jogador_direita.nome_jogador,
                "cartas_finais": cartas_destino,
            },
        }

    except Exception as e:
        print("=" * 80)
        print("ERRO AO TROCAR CARTAS ENTRE JOGADORES (DIREITA)")
        print(f"Jogador origem: {getattr(jogador, 'nome_jogador', '?')}")
        print(f"id_carta_jogador: {id_carta_jogador}")
        print(f"id_carta_direita: {id_carta_direita}")
        print("Traceback:")
        traceback.print_exc()
        print("=" * 80)
        return JsonResponse(
            {
                "erro": "Erro interno ao processar a troca de cartas (direita).",
                "detalhes": str(e),
                "traceback": traceback.format_exc(),
            },
            status=400,
        )


def roubar_carta(jogador, jogador_destino, id_carta):
    """
    Rouba uma carta específica de um jogador destino.
    """
    partida = jogador.id_partida
    if not partida:
        return {"mensagem": "Jogador não está vinculado a uma partida."}

    # Baralhos
    baralho_origem, _ = Baralho.objects.get_or_create(
        id_jogador=jogador, id_partida=partida
    )
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=partida
    )

    cartas_origem = (
        json.loads(baralho_origem.lista_de_cartas)
        if baralho_origem.lista_de_cartas
        else []
    )
    cartas_destino = (
        json.loads(baralho_destino.lista_de_cartas)
        if baralho_destino.lista_de_cartas
        else []
    )

    if id_carta not in cartas_destino:
        return {
            "mensagem": f"Carta {id_carta} não encontrada no baralho do jogador alvo."
        }

    # Remove do destino e adiciona ao ladrão
    cartas_destino.remove(id_carta)
    cartas_origem.append(id_carta)

    baralho_origem.lista_de_cartas = json.dumps(cartas_origem)
    baralho_destino.lista_de_cartas = json.dumps(cartas_destino)
    baralho_origem.save()
    baralho_destino.save()

    mensagem = f"{jogador.nome_jogador} roubou a carta {id_carta} de {jogador_destino.nome_jogador}."

    # Notificação para o jogador roubado
    criar_notificacao(jogador, jogador_destino, mensagem)

    return {
        "mensagem": mensagem,
        "jogador_origem": {
            "id": jogador.id_jogador,
            "nome": jogador.nome_jogador,
            "cartas_finais": cartas_origem,
        },
        "jogador_destino": {
            "id": jogador_destino.id_jogador,
            "nome": jogador_destino.nome_jogador,
            "cartas_finais": cartas_destino,
        },
    }


def roubar_jogador_esquerda(jogador, id_carta):
    """
    Rouba uma carta de quem está imediatamente à esquerda.
    """
    partida = jogador.id_partida
    ordem_cores = ["amarelo", "azul", "preto", "roxo"]

    cor_atual = jogador.cor_jogador.lower()
    idx_atual = ordem_cores.index(cor_atual)

    prox_idx = (idx_atual - 1) % len(ordem_cores)
    jogador_destino_id = None
    tentativas = 0
    while tentativas < len(ordem_cores):
        cor_prox = ordem_cores[prox_idx]
        jogador_destino_id = getattr(partida, f"id_jogador_{cor_prox}", None)
        if jogador_destino_id:
            break
        prox_idx = (prox_idx - 1) % len(ordem_cores)
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Nenhum jogador válido encontrado para roubo."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)
    return roubar_carta(jogador, jogador_destino, id_carta)


def roubar_jogador_direita(jogador, id_carta):
    """
    Rouba uma carta de quem está imediatamente à direita.
    """
    partida = jogador.id_partida
    ordem_cores = ["amarelo", "azul", "preto", "roxo"]

    cor_atual = jogador.cor_jogador.lower()
    idx_atual = ordem_cores.index(cor_atual)

    prox_idx = (idx_atual + 1) % len(ordem_cores)
    jogador_destino_id = None
    tentativas = 0
    while tentativas < len(ordem_cores):
        cor_prox = ordem_cores[prox_idx]
        jogador_destino_id = getattr(partida, f"id_jogador_{cor_prox}", None)
        if jogador_destino_id:
            break
        prox_idx = (prox_idx + 1) % len(ordem_cores)
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Nenhum jogador válido encontrado para roubo."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)
    return roubar_carta(jogador, jogador_destino, id_carta)


def roubar_jogador_geral(jogador, id_jogador_destino, id_carta):
    """
    Rouba uma carta de um jogador específico (id_jogador_destino).
    """
    try:
        jogador_destino = Jogador.objects.get(id_jogador=id_jogador_destino)
    except Jogador.DoesNotExist:
        return {"mensagem": "Jogador alvo não encontrado."}

    return roubar_carta(jogador, jogador_destino, id_carta)


def doar_carta(jogador, id_jogador_destino, id_carta):
    """
    Doe uma carta específica a outro jogador.
    """
    try:
        jogador_destino = Jogador.objects.get(id_jogador=id_jogador_destino)
    except Jogador.DoesNotExist:
        return {"mensagem": "Jogador destino não encontrado."}

    partida = jogador.id_partida
    if not partida:
        return {"mensagem": "Jogador não está vinculado a uma partida."}

    # Carrega os baralhos
    baralho_origem, _ = Baralho.objects.get_or_create(
        id_jogador=jogador, id_partida=partida
    )
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=partida
    )

    cartas_origem = (
        json.loads(baralho_origem.lista_de_cartas)
        if baralho_origem.lista_de_cartas
        else []
    )
    cartas_destino = (
        json.loads(baralho_destino.lista_de_cartas)
        if baralho_destino.lista_de_cartas
        else []
    )

    if id_carta not in cartas_origem:
        return {"mensagem": f"Carta {id_carta} não encontrada no baralho do jogador."}

    # Remove a carta do jogador origem
    cartas_origem.remove(id_carta)

    # Adiciona ao jogador destino
    cartas_destino.append(id_carta)

    # Salva os baralhos
    baralho_origem.lista_de_cartas = json.dumps(cartas_origem)
    baralho_destino.lista_de_cartas = json.dumps(cartas_destino)
    baralho_origem.save()
    baralho_destino.save()

    # Monta mensagem
    mensagem = f"{jogador.nome_jogador} doou a carta {id_carta} para {jogador_destino.nome_jogador}."

    # Cria notificação
    criar_notificacao(jogador, jogador_destino, mensagem)

    return {
        "mensagem": mensagem,
        "jogador_origem": {
            "id": jogador.id_jogador,
            "nome": jogador.nome_jogador,
            "cartas_finais": cartas_origem,
        },
        "jogador_destino": {
            "id": jogador_destino.id_jogador,
            "nome": jogador_destino.nome_jogador,
            "cartas_finais": cartas_destino,
        },
    }


def entregar_carta_jogador_direita(jogador, casa):
    """
    Pega 1 carta aleatória disponível e entrega ao jogador à direita.
    Registra notificação para o jogador destino.
    Percorre a sequência de cores até encontrar um jogador válido.
    """
    controle = ControlePartida.objects.filter(id_partida=jogador.id_partida).first()
    if not controle:
        raise Exception("Controle da partida não encontrado.")

    entregues_ids = []
    if controle.cartas_jogadores:
        entregues_ids += json.loads(controle.cartas_jogadores)
    if controle.cartas_descartadas:
        entregues_ids += json.loads(controle.cartas_descartadas)

    cores = ["amarelo", "azul", "preto", "roxo"]
    cor_atual = jogador.cor_jogador.lower().strip()
    idx_atual = cores.index(cor_atual)

    # Busca jogador à direita válido
    prox_idx = (idx_atual + 1) % len(cores)
    jogador_destino_id = None
    tentativas = 0

    while tentativas < len(cores):
        cor_prox = cores[prox_idx]
        candidato_id = getattr(jogador.id_partida, f"id_jogador_{cor_prox}", None)

        # precisa ser um jogador válido e diferente do atual
        if candidato_id and candidato_id != jogador.id_jogador:
            jogador_destino_id = candidato_id
            break

        prox_idx = (prox_idx + 1) % len(cores)
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Não há jogador válido à direita para receber a carta."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)

    # Seleciona carta aleatória disponível
    todas_cartas = BaralhoCadastro.objects.all()
    carta_escolhida = next(
        (c for c in todas_cartas if c.id_carta not in entregues_ids), None
    )
    if not carta_escolhida:
        return {"mensagem": "Não há cartas disponíveis para entregar."}

    entregues_ids.append(carta_escolhida.id_carta)

    # Adiciona carta ao baralho do jogador destino
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=jogador.id_partida
    )
    lista_cartas = (
        json.loads(baralho_destino.lista_de_cartas)
        if baralho_destino.lista_de_cartas
        else []
    )
    lista_cartas.append(carta_escolhida.id_carta)
    baralho_destino.lista_de_cartas = json.dumps(lista_cartas)
    baralho_destino.save()

    # Atualiza controle
    controle.cartas_jogadores = json.dumps(entregues_ids)
    controle.save()

    # Cria notificação
    Notificacao.objects.create(
        id_jogador_origem=jogador,
        id_jogador_destino=jogador_destino,
        id_partida=jogador.id_partida.id_partida,
        mensagem=f"Recebeu uma carta de {jogador.nome_jogador}",
    )

    return {
        "cartas_adicionadas": [
            {
                "id_carta": carta_escolhida.id_carta,
                "nome": carta_escolhida.nome_carta,
                "tipo": carta_escolhida.tipo_carta,
            }
        ]
    }


def entregar_carta_jogador_frente(jogador, casa):
    """
    Pega 1 carta aleatória disponível e entrega ao jogador à frente (pula 1 jogador).
    Registra notificação para o jogador destino.
    Percorre a sequência de cores até encontrar um jogador válido diferente do atual.
    """
    controle = ControlePartida.objects.filter(id_partida=jogador.id_partida).first()
    if not controle:
        raise Exception("Controle da partida não encontrado.")

    entregues_ids = []
    if controle.cartas_jogadores:
        entregues_ids += json.loads(controle.cartas_jogadores)
    if controle.cartas_descartadas:
        entregues_ids += json.loads(controle.cartas_descartadas)

    cores = ["amarelo", "azul", "preto", "roxo"]
    cor_atual = jogador.cor_jogador.lower().strip()
    idx_atual = cores.index(cor_atual)

    # Busca jogador à frente válido (pula 1)
    prox_idx = (idx_atual + 2) % len(cores)
    jogador_destino_id = None
    tentativas = 0

    while tentativas < len(cores):
        cor_prox = cores[prox_idx]
        candidato_id = getattr(jogador.id_partida, f"id_jogador_{cor_prox}", None)

        # precisa ser um jogador válido e DIFERENTE do atual
        if candidato_id and int(candidato_id) != int(jogador.id_jogador):
            jogador_destino_id = candidato_id
            break

        # pula para o próximo
        prox_idx = (prox_idx + 1) % len(cores)
        tentativas += 1

    if not jogador_destino_id:
        return {"mensagem": "Não há jogador válido à frente para receber a carta."}

    jogador_destino = Jogador.objects.get(id_jogador=jogador_destino_id)

    # Seleciona carta aleatória disponível
    todas_cartas = BaralhoCadastro.objects.all()
    carta_escolhida = next(
        (c for c in todas_cartas if c.id_carta not in entregues_ids), None
    )
    if not carta_escolhida:
        return {"mensagem": "Não há cartas disponíveis para entregar."}

    entregues_ids.append(carta_escolhida.id_carta)

    # Adiciona carta ao baralho do jogador destino
    baralho_destino, _ = Baralho.objects.get_or_create(
        id_jogador=jogador_destino, id_partida=jogador.id_partida
    )
    lista_cartas = (
        json.loads(baralho_destino.lista_de_cartas)
        if baralho_destino.lista_de_cartas
        else []
    )
    lista_cartas.append(carta_escolhida.id_carta)
    baralho_destino.lista_de_cartas = json.dumps(lista_cartas)
    baralho_destino.save()

    # Atualiza controle
    controle.cartas_jogadores = json.dumps(entregues_ids)
    controle.save()

    # Cria notificação
    Notificacao.objects.create(
        id_jogador_origem=jogador,
        id_jogador_destino=jogador_destino,
        id_partida=jogador.id_partida.id_partida,
        mensagem=f"Recebeu uma carta de {jogador.nome_jogador}",
    )

    return {
        "cartas_adicionadas": [
            {
                "id_carta": carta_escolhida.id_carta,
                "nome": carta_escolhida.nome_carta,
                "tipo": carta_escolhida.tipo_carta,
            }
        ]
    }


def criar_notificacao(jogador_origem, jogador_destino, mensagem):
    """
    Cria uma notificação entre jogador_origem e jogador_destino.
    """
    notificacao = Notificacao.objects.create(
        id_jogador_origem=jogador_origem,
        id_jogador_destino=jogador_destino,
        id_partida=jogador_origem.id_partida.id_partida,
        mensagem=mensagem,
        necessita_atualizar=True,
        processado=False,
    )
    return notificacao


def verificar_cartas_baralho(jogador_id):
    # Caso as cartas de evidencia não estejam na lista_de_cartas do usuario
    # Elas serão zeradas nos campos id_carta_inicio/meio/final
    try:
        baralho = Baralho.objects.get(id_jogador_id=jogador_id)

        # Tenta converter lista_de_cartas em lista real
        try:
            lista_cartas = json.loads(baralho.lista_de_cartas or "[]")
        except json.JSONDecodeError:
            print(
                f"Lista de cartas inválida para jogador {jogador_id}. Resetando lista."
            )
            lista_cartas = []

        # Guarda o estado inicial
        alterado = False

        # Verifica id_carta_inicio
        if baralho.id_carta_inicio not in lista_cartas:
            baralho.id_carta_inicio = 0
            alterado = True

        # Verifica id_carta_meio
        if baralho.id_carta_meio not in lista_cartas:
            baralho.id_carta_meio = 0
            alterado = True

        # Verifica id_carta_fim
        if baralho.id_carta_fim not in lista_cartas:
            baralho.id_carta_fim = 0
            alterado = True

        # Se houve mudança, salva
        if alterado:
            with transaction.atomic():
                baralho.save()
            # print(f"✅ Baralho do jogador {jogador_id} atualizado com sucesso.")
        # else:
        # print(f"ℹ️ Nenhuma alteração necessária para o jogador {jogador_id}.")

    except Baralho.DoesNotExist:
        print(f"Nenhum baralho encontrado para o jogador {jogador_id}.")


@csrf_exempt
def criar_elogio(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        id_origem = data.get("jogador_origem")
        id_destino = data.get("jogador_destino")
        mensagem = data.get("mensagem")

        if not (id_origem and id_destino and mensagem):
            return JsonResponse({"erro": "Campos obrigatórios faltando"}, status=400)

        # Recupera jogadores
        jogador_origem = Jogador.objects.get(id_jogador=id_origem)
        jogador_destino = Jogador.objects.get(id_jogador=id_destino)

        # Partida do jogador origem
        partida = jogador_origem.id_partida
        if not partida:
            return JsonResponse(
                {"erro": "Jogador de origem não está em uma partida"}, status=400
            )

        # Cria elogio
        elogio = Elogio.objects.create(
            id_partida=partida,
            jogador_origem=jogador_origem,
            jogador_destino=jogador_destino,
            mensagem=mensagem,
        )

        # Cria notificação para o jogador destino
        texto_notificacao = f"Você recebeu um elogio de {jogador_origem.nome_jogador}"
        Notificacao.objects.create(
            id_jogador_origem=jogador_origem,
            id_jogador_destino=jogador_destino,
            id_partida=partida.id_partida,
            mensagem=texto_notificacao,
            necessita_atualizar=True,
            processado=False,
        )

        return JsonResponse(
            {
                "sucesso": True,
                "mensagem": "Elogio criado com sucesso",
                "elogio": {
                    "id": elogio.id_elogio,
                    "partida": partida.id_partida,
                    "origem": jogador_origem.nome_jogador,
                    "destino": jogador_destino.nome_jogador,
                    "mensagem": elogio.mensagem,
                    "criado_em": elogio.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }
        )

    except Jogador.DoesNotExist:
        return JsonResponse({"erro": "Jogador não encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)


@csrf_exempt
def listar_elogios_partida(request, id_partida):
    if request.method != "GET":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        # Verifica se a partida existe
        partida = Partida.objects.get(id_partida=id_partida)

        # Filtra elogios da partida
        elogios = Elogio.objects.filter(id_partida=partida).order_by("criado_em")

        elogios_list = [
            {
                "id_elogio": elogio.id_elogio,
                "origem": elogio.jogador_origem.nome_jogador,
                "destino": elogio.jogador_destino.nome_jogador,
                "mensagem": elogio.mensagem,
                "criado_em": elogio.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for elogio in elogios
        ]

        return JsonResponse({"elogios": elogios_list})

    except Partida.DoesNotExist:
        return JsonResponse({"erro": "Partida não encontrada"}, status=404)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)


@api_view(["POST"])
def atualizar_cartas_baralho(request):
    """
    Atualiza as colunas de id_carta_inicio, id_carta_meio ou id_carta_fim
    do Baralho associado ao jogador.

    Parâmetros esperados:
    - id_jogador: int (obrigatório)
    - controle: int (1 = início, 2 = meio, 3 = fim)
    - id_carta: int (obrigatório)
    """
    try:
        id_jogador = request.data.get("id_jogador")
        controle = request.data.get("controle")
        id_carta = request.data.get("id_carta")

        # Validação básica
        if not all([id_jogador, controle, id_carta]):
            return Response(
                {"erro": "id_jogador, controle e id_carta são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Conversões e validações de tipo
        try:
            id_jogador = int(id_jogador)
            controle = int(controle)
            id_carta = int(id_carta)
        except ValueError:
            return Response(
                {"erro": "Todos os campos devem ser números inteiros."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Busca o jogador e seu baralho
        jogador = Jogador.objects.get(id_jogador=id_jogador)
        baralho = Baralho.objects.get(id_jogador=jogador)

        # Atualiza campo conforme o valor de controle
        if controle == 1:
            baralho.id_carta_inicio = id_carta
            campo = "id_carta_inicio"
        elif controle == 2:
            baralho.id_carta_meio = id_carta
            campo = "id_carta_meio"
        elif controle == 3:
            baralho.id_carta_fim = id_carta
            campo = "id_carta_fim"
        else:
            return Response(
                {
                    "erro": "Valor de controle inválido. Use 1 (início), 2 (meio) ou 3 (fim)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        baralho.save()

        return Response(
            {
                "mensagem": f"Carta {id_carta} adicionada com sucesso em {campo}.",
                "baralho": {
                    "id_jogador": jogador.id_jogador,
                    "id_carta_inicio": baralho.id_carta_inicio,
                    "id_carta_meio": baralho.id_carta_meio,
                    "id_carta_fim": baralho.id_carta_fim,
                },
            },
            status=status.HTTP_200_OK,
        )

    except Jogador.DoesNotExist:
        return Response(
            {"erro": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Baralho.DoesNotExist:
        return Response(
            {"erro": "Baralho não encontrado para este jogador."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def consultar_cartas_evidencia(request, id_jogador):
    """
    Consulta as cartas em evidência de um jogador (início, meio e fim).
    Retorna id_carta, nome_carta e descricao_carta de cada uma.
    """
    try:
        # Busca o jogador
        jogador = Jogador.objects.get(id_jogador=id_jogador)

        # Busca o baralho do jogador
        baralho = Baralho.objects.get(id_jogador=jogador)

        # Função auxiliar para buscar dados da carta
        def get_carta_info(id_carta):
            if id_carta == 0:
                return None  # não há carta definida
            try:
                carta = BaralhoCadastro.objects.get(id_carta=id_carta)
                return {
                    "id_carta": carta.id_carta,
                    "nome_carta": carta.nome_carta,
                    "descricao_carta": carta.descricao_carta,
                    "cor_carta": carta.cor_carta,
                }
            except BaralhoCadastro.DoesNotExist:
                return None

        return Response(
            {
                "id_jogador": jogador.id_jogador,
                "cartas_evidencia": {
                    "inicio": get_carta_info(baralho.id_carta_inicio),
                    "meio": get_carta_info(baralho.id_carta_meio),
                    "fim": get_carta_info(baralho.id_carta_fim),
                },
            },
            status=status.HTTP_200_OK,
        )

    except Jogador.DoesNotExist:
        return Response(
            {"erro": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Baralho.DoesNotExist:
        return Response(
            {"erro": "Baralho não encontrado para este jogador."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def atualizar_controle_jogador(request):
    """
    Atualiza o registro de ControleJogador conforme id_gravacao:
    - id_gravacao = 1 -> acresce valor em sem_jogar_rodadas
    - id_gravacao = 2 -> acresce valor em vezes_extra
    """
    try:
        id_partida = request.data.get("id_partida")
        id_jogador = request.data.get("id_jogador")
        valor = request.data.get("valor")
        id_gravacao = request.data.get("id_gravacao")

        # Valida parâmetros obrigatórios
        if not all([id_partida, id_jogador, valor, id_gravacao]):
            return Response(
                {
                    "erro": "id_partida, id_jogador, valor e id_gravacao são obrigatórios."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Converte valor para inteiro
        try:
            valor = int(valor)
        except ValueError:
            return Response(
                {"erro": "valor deve ser um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Busca ou cria registro de controle
        partida = Partida.objects.get(id_partida=id_partida)
        jogador = Jogador.objects.get(id_jogador=id_jogador)
        controle, _ = ControleJogador.objects.get_or_create(
            id_partida=partida, id_jogador=jogador
        )

        # Atualiza coluna correta
        if id_gravacao == 1:
            controle.sem_jogar_rodadas += valor
        elif id_gravacao == 2:
            controle.vezes_extra += valor
        else:
            return Response(
                {"erro": "id_gravacao inválido. Use 1 ou 2."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        controle.save()

        return Response(
            {
                "mensagem": "Controle atualizado com sucesso.",
                "sem_jogar_rodadas": controle.sem_jogar_rodadas,
                "vezes_extra": controle.vezes_extra,
            },
            status=status.HTTP_200_OK,
        )

    except Partida.DoesNotExist:
        return Response(
            {"erro": "Partida não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )
    except Jogador.DoesNotExist:
        return Response(
            {"erro": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def consultar_controle_jogador(request, id_jogador, id_partida):
    """
    Consulta os valores de sem_jogar_rodadas e vezes_extra de um jogador em uma partida.
    """
    try:
        jogador = Jogador.objects.get(id_jogador=id_jogador)
        partida = Partida.objects.get(id_partida=id_partida)

        controle = ControleJogador.objects.filter(
            id_jogador=jogador, id_partida=partida
        ).first()

        if not controle:
            return Response(
                {
                    "mensagem": "Controle do jogador não encontrado.",
                    "sem_jogar_rodadas": 0,
                    "vezes_extra": 0,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "id_jogador": jogador.id_jogador,
                "id_partida": partida.id_partida,
                "sem_jogar_rodadas": controle.sem_jogar_rodadas,
                "vezes_extra": controle.vezes_extra,
            },
            status=status.HTTP_200_OK,
        )

    except Jogador.DoesNotExist:
        return Response(
            {"erro": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Partida.DoesNotExist:
        return Response(
            {"erro": "Partida não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def decrementar_controle_jogador_campo(request):
    """
    Decrementa 1 no campo especificado do ControleJogador.

    Request JSON:
    {
        "id_jogador": 1,
        "id_partida": 2,
        "id_gravacao": 1  # 1 = sem_jogar_rodadas, 2 = vezes_extra
    }
    """
    try:
        id_jogador = request.data.get("id_jogador")
        id_partida = request.data.get("id_partida")
        id_gravacao = request.data.get("id_gravacao")

        if not id_jogador or not id_partida or not id_gravacao:
            return Response(
                {"erro": "id_jogador, id_partida e id_gravacao são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        jogador = Jogador.objects.get(id_jogador=id_jogador)
        partida = Partida.objects.get(id_partida=id_partida)

        controle, created = ControleJogador.objects.get_or_create(
            id_jogador=jogador, id_partida=partida
        )

        if id_gravacao == 1:
            if controle.sem_jogar_rodadas > 0:
                controle.sem_jogar_rodadas -= 1
        elif id_gravacao == 2:
            if controle.vezes_extra > 0:
                controle.vezes_extra -= 1
        else:
            return Response(
                {"erro": "id_gravacao inválido. Use 1 ou 2."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        controle.save()

        return Response(
            {
                "id_jogador": jogador.id_jogador,
                "id_partida": partida.id_partida,
                "sem_jogar_rodadas": controle.sem_jogar_rodadas,
                "vezes_extra": controle.vezes_extra,
                "mensagem": "Campo decrementado com sucesso.",
            },
            status=status.HTTP_200_OK,
        )

    except Jogador.DoesNotExist:
        return Response(
            {"erro": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Partida.DoesNotExist:
        return Response(
            {"erro": "Partida não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@require_GET
def notificacoes_pendentes_partida(request, partida_id):
    """
    Retorna todas as notificações pendentes de uma partida.
    """
    notificacoes = Notificacao.objects.filter(
        id_partida=partida_id,
        processado=False,
        necessita_atualizar=True,
    ).order_by("-criado_em")

    data = [
        {
            "id": n.id_notificacao,
            "jogador_origem": n.id_jogador_origem.id_jogador,
            "jogador_destino": n.id_jogador_destino.id_jogador,
            "mensagem": n.mensagem,
            "criado_em": n.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for n in notificacoes
    ]

    return JsonResponse({"pendentes": data})


@require_GET
def notificacoes_pendentes_jogador(request, jogador_id, partida_id):
    """
    Retorna as notificações pendentes de um jogador em uma partida específica.
    """

    verificar_cartas_baralho(jogador_id)

    verificar_vitoria_e_notificar()

    notificacoes = Notificacao.objects.filter(
        id_jogador_destino_id=jogador_id,
        id_partida=partida_id,
        processado=False,
        necessita_atualizar=True,
    ).order_by("-criado_em")

    data = [
        {
            "id": n.id_notificacao,
            "mensagem": n.mensagem,
            "criado_em": n.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for n in notificacoes
    ]

    return JsonResponse({"pendentes": data})


@csrf_exempt
@require_POST
def marcar_notificacao_processada(request):
    """
    Marca uma notificação como processada a partir do id_notificacao enviado no corpo da requisição.
    Exemplo de requisição:
    POST /notificacoes/processar/
    {
        "id_notificacao": 5
    }
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
        id_notificacao = body.get("id_notificacao")

        if not id_notificacao:
            return JsonResponse({"erro": "id_notificacao é obrigatório"}, status=400)

        notificacao = Notificacao.objects.filter(id_notificacao=id_notificacao).first()
        if not notificacao:
            return JsonResponse({"erro": "Notificação não encontrada"}, status=404)

        notificacao.processado = True
        notificacao.necessita_atualizar = False
        notificacao.save()

        return JsonResponse(
            {"mensagem": f"Notificação {id_notificacao} marcada como processada."},
            status=200,
        )

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)


# ======================================================
# ENDPOINT PRINCIPAL
# ======================================================


@api_view(["POST"])
def executar_acao_casa(request):
    try:
        id_jogador = request.data.get("id_jogador")
        id_casa = request.data.get("id_casa")
        id_jogador_destino = request.data.get("id_jogador_destino")  # Opcional
        id_carta = request.data.get("id_carta")  # Opcional

        if not id_jogador or not id_casa:
            return Response(
                {"erro": "id_jogador e id_casa são obrigatórios."}, status=400
            )

        jogador = Jogador.objects.get(id_jogador=id_jogador)
        casa = TabuleiroCadastro.objects.get(id_casa=id_casa)
        acao = casa.acao

        resultado = {}

        # Ações padrão
        if acao.id_acao in [23, 24, 25]:
            resultado = perder_carta(jogador, casa, acao)

        elif acao.id_acao in [2, 3, 4]:
            resultado = ganhar_carta(jogador, casa, acao)

        elif acao.id_acao == 5:
            tipo_carta = request.data.get("tipo_carta")
            resultado = ganhar_carta(jogador, casa, acao, tipo_carta=tipo_carta)

        elif acao.id_acao == 6:
            resultado = trocar_com_jogador_frente(jogador, casa, acao)

        elif acao.id_acao == 7:
            resultado = trocar_com_jogador_direita(jogador, casa, acao)

        elif acao.id_acao == 8:
            resultado = trocar_com_jogador_esquerda(jogador, casa, acao)

        elif acao.id_acao == 10:
            if not id_jogador_destino or not id_carta:
                return Response(
                    {"erro": "id_jogador_destino e id_carta são obrigatórios."},
                    status=400,
                )
            resultado = doar_carta(jogador, id_jogador_destino, id_carta)

        elif acao.id_acao == 13:
            if not id_carta:
                return Response({"erro": "id_carta é obrigatório."}, status=400)
            resultado = roubar_jogador_esquerda(jogador, id_carta)

        elif acao.id_acao == 14:
            if not id_carta:
                return Response({"erro": "id_carta é obrigatório."}, status=400)
            resultado = roubar_jogador_direita(jogador, id_carta)

        elif acao.id_acao == 15:
            if not id_jogador_destino or not id_carta:
                return Response(
                    {"erro": "id_jogador_destino e id_carta são obrigatórios."},
                    status=400,
                )
            resultado = roubar_jogador_geral(jogador, id_jogador_destino, id_carta)

        elif acao.id_acao == 16:
            resultado = entregar_carta_jogador_frente(jogador, casa)

        elif acao.id_acao == 17:
            resultado = entregar_carta_jogador_direita(jogador, casa)

        elif acao.id_acao == 18:  # Troca de carta com jogador à esquerda
            id_carta_jogador = request.data.get("id_carta_jogador")
            id_carta_esquerda = request.data.get("id_carta_esquerda")

            if not id_carta_jogador or not id_carta_esquerda:
                return Response(
                    {"erro": "id_carta_jogador e id_carta_esquerda são obrigatórios."},
                    status=400,
                )

            resultado = trocar_carta_com_esquerda(
                jogador, id_carta_jogador, id_carta_esquerda
            )

        elif acao.id_acao == 19:  # Troca de carta com jogador à esquerda
            id_carta_jogador = request.data.get("id_carta_jogador")
            id_carta_direita = request.data.get("id_carta_direita")

            if not id_carta_jogador or not id_carta_direita:
                return Response(
                    {"erro": "id_carta_jogador e id_carta_direita são obrigatórios."},
                    status=400,
                )

            resultado = trocar_carta_com_direita(
                jogador, id_carta_jogador, id_carta_direita
            )

        # Retorno unificado
        return Response(
            {
                "id_jogador": jogador.id_jogador,
                "nova_posicao": {
                    "id_casa": casa.id_casa,
                    "nome_casa": casa.nome_casa,
                },
                **resultado,
            },
            status=200,
        )

    except Jogador.DoesNotExist:
        return Response({"erro": "Jogador não encontrado."}, status=404)

    except TabuleiroCadastro.DoesNotExist:
        return Response({"erro": "Casa do tabuleiro não encontrada."}, status=404)

    except Exception as e:
        print("=== ERRO NO EXECUTAR ACAO CASA ===")
        traceback.print_exc()
        print("=== FIM DO ERRO ===")
        return Response({"erro": str(e)}, status=500)
