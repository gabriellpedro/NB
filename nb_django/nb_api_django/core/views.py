import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import (
    AcaoCadastro,
    Baralho,
    BaralhoCadastro,
    ControlePartida,
    Jogador,
    Partida,
    TabuleiroCadastro,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import api_view


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

    # Todas as cartas disponíveis no cadastro
    todas_cartas = list(BaralhoCadastro.objects.values_list("id_carta", flat=True))

    # Filtra as cartas disponíveis: não podem estar em uso nem descartadas
    cartas_disponiveis = list(
        set(todas_cartas) - set(cartas_em_uso) - set(cartas_descartadas)
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


@api_view(["POST"])
def executar_acao_casa(request):
    try:
        id_jogador = request.data.get("id_jogador")
        id_casa = request.data.get("id_casa")

        if not id_jogador or not id_casa:
            return Response(
                {"erro": "id_jogador e id_casa são obrigatórios."}, status=400
            )

        # Busca jogador e casa
        jogador = Jogador.objects.get(id_jogador=id_jogador)
        casa = TabuleiroCadastro.objects.get(id_casa=id_casa)
        acao = casa.acao

        # Apenas para ações 2, 3, 4, 5
        if acao.id_acao not in [2, 3, 4, 5]:
            return Response(
                {"erro": "Ação não distribuível automaticamente."}, status=400
            )

        # Busca controle da partida (assumindo 1 partida ativa)
        controle = ControlePartida.objects.filter(id_partida=jogador.id_partida).first()
        if not controle:
            return Response({"erro": "Controle da partida não encontrado."}, status=400)

        # Lista de cartas já entregues (jogadores + descartadas)
        entregues_ids = []
        if controle.cartas_jogadores:
            entregues_ids += json.loads(controle.cartas_jogadores)
        if controle.cartas_descartadas:
            entregues_ids += json.loads(controle.cartas_descartadas)

        # Busca ou cria baralho do jogador
        baralho, _ = Baralho.objects.get_or_create(
            id_jogador=jogador, id_partida=jogador.id_partida
        )
        lista_cartas_jogador = (
            json.loads(baralho.lista_de_cartas) if baralho.lista_de_cartas else []
        )

        cartas_adicionadas = []

        # Função interna para buscar carta disponível do tipo
        def buscar_carta_disponivel(tipo):
            todas_cartas = BaralhoCadastro.objects.filter(tipo_carta=tipo)
            for c in todas_cartas:
                if c.id_carta not in entregues_ids:
                    entregues_ids.append(c.id_carta)  # marca como entregue
                    return c
            return None

        # Define tipos de cartas a distribuir conforme id_acao
        if acao.id_acao == 2:
            tipos_a_distribuir = ["final"]
        elif acao.id_acao == 3:
            tipos_a_distribuir = ["meio"]
        elif acao.id_acao == 4:
            tipos_a_distribuir = ["inicio"]
        elif acao.id_acao == 5:
            tipos_a_distribuir = ["inicio", "meio", "final"]

        # Distribui cartas disponíveis
        for tipo in tipos_a_distribuir:
            carta = buscar_carta_disponivel(tipo)
            if carta:
                lista_cartas_jogador.append(carta.id_carta)
                cartas_adicionadas.append(carta)
                print(
                    f"Adicionada carta {carta.nome_carta} ({carta.tipo_carta}) ao jogador {jogador.nome_jogador}"
                )
            else:
                print(f"Nenhuma carta disponível do tipo {tipo}")

        # Salva lista de cartas do jogador
        baralho.lista_de_cartas = json.dumps(lista_cartas_jogador)
        baralho.save()

        # Atualiza controle global de cartas entregues
        controle.cartas_jogadores = json.dumps(entregues_ids)
        controle.save()

        return Response(
            {
                "id_jogador": jogador.id_jogador,
                "nova_posicao": {"id_casa": casa.id_casa, "nome_casa": casa.nome_casa},
                "cartas_adicionadas": [
                    {"id_carta": c.id_carta, "nome": c.nome_carta, "tipo": c.tipo_carta}
                    for c in cartas_adicionadas
                ],
            }
        )

    except Jogador.DoesNotExist:
        return Response({"erro": "Jogador não encontrado."}, status=404)
    except TabuleiroCadastro.DoesNotExist:
        return Response({"erro": "Casa do tabuleiro não encontrada."}, status=404)
    except Exception as e:
        return Response({"erro": str(e)}, status=500)
