import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import Baralho, BaralhoCadastro, ControlePartida, Jogador, Partida
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


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
            return Response({"error": "Nome e Cor do jogador são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Se não veio id_partida → cria nova partida
        if not id_partida:
            partida = Partida.objects.create()
        else:
            try:
                partida = Partida.objects.get(id_partida=id_partida)
            except Partida.DoesNotExist:
                return Response({"error": "Partida não encontrada."},
                                status=status.HTTP_404_NOT_FOUND)

        # Verifica se já existe jogador com a mesma cor nesta partida
        cor_field = f"id_jogador_{cor_jogador.lower()}"
        if hasattr(partida, cor_field) and getattr(partida, cor_field):
            return Response({"error": f"A cor {cor_jogador} já está ocupada nesta partida."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Cria o jogador
        jogador = Jogador.objects.create(
            nome_jogador=nome_jogador,
            cor_jogador=cor_jogador,
            id_partida=partida
        )

        # Atualiza a partida com o jogador na cor correta
        if hasattr(partida, cor_field):
            setattr(partida, cor_field, jogador.id_jogador)
            partida.save()

        criar_baralho_para_jogador(jogador, partida)

        return Response({
            "message": "Jogador criado com sucesso!",
            "jogador": {
                "id_jogador": jogador.id_jogador,
                "nome_jogador": jogador.nome_jogador,
                "cor_jogador": jogador.cor_jogador,
                "id_partida": partida.id_partida,
            }
        }, status=status.HTTP_201_CREATED)

def criar_baralho_para_jogador(jogador, partida, quantidade=2):
    """
    Cria um baralho para o jogador, vinculando-o à partida e distribuindo cartas.
    """
    # Recupera ou cria um baralho para o jogador
    baralho = Baralho.objects.create(
        id_jogador=jogador,
        id_partida=partida,
    )

    controle, _ = ControlePartida.objects.get_or_create(id_partida=partida)

    # Cartas já em circulação (globais)
    cartas_em_uso = json.loads(controle.cartas_jogadores or "[]")

    # Pega cartas disponíveis do cadastro
    todas_cartas = list(BaralhoCadastro.objects.values_list("id_carta", flat=True))
    cartas_disponiveis = list(set(todas_cartas) - set(cartas_em_uso))

    # Sorteia as cartas
    cartas_sorteadas = random.sample(cartas_disponiveis, quantidade)

    # Vincula as cartas ao baralho do jogador
    baralho.lista_de_cartas = json.dumps(cartas_sorteadas)
    baralho.save()

    # Atualiza o jogador com o ID do baralho
    jogador.id_baralho = baralho.id_baralho
    jogador.save()

    # Atualiza a partida para registrar essas cartas como em circulação
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
    """

    def get(self, request, id_jogador):
        try:
            jogador = Jogador.objects.get(id_jogador=id_jogador)
        except Jogador.DoesNotExist:
            return Response({"error": "Jogador não encontrado."}, status=status.HTTP_404_NOT_FOUND)

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
                    cartas_detalhes.append({
                        "id_carta": carta.id_carta,
                        "nome_carta": carta.nome_carta,
                        "tipo_carta": carta.tipo_carta,
                        "cor_carta": carta.cor_carta,
                        "descricao_carta": carta.descricao_carta,
                    })

            except Baralho.DoesNotExist:
                cartas_detalhes = []

        # Monta a resposta
        data = {
            "id_partida": partida_id,
            "id_jogador": jogador.id_jogador,
            "nome_jogador": jogador.nome_jogador,
            "cor_jogador": jogador.cor_jogador,
            "id_casa": jogador.id_casa,
            "cartas": cartas_detalhes,
        }

        return Response(data, status=status.HTTP_200_OK)