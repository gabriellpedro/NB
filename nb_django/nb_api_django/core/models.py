import json
from django.db import models

class Partida(models.Model):
    id_partida = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    id_jogador_amarelo = models.IntegerField(null=True, blank=True)
    id_jogador_azul = models.IntegerField(null=True, blank=True)
    id_jogador_preto = models.IntegerField(null=True, blank=True)
    id_jogador_roxo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Partida {self.id_partida}"


class ControlePartida(models.Model):
    id_partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    ultimo_jogar = models.IntegerField(null=True, blank=True)
    proximo_jogar = models.IntegerField(null=True, blank=True)

    cartas_jogadores = models.TextField(default="[]")
    cartas_descartadas = models.TextField(default="[]")

    def add_cartas_jogadores(self, novas_cartas):
        lista = json.loads(self.cartas_jogadores)
        lista.extend(novas_cartas)
        self.cartas_jogadores = json.dumps(lista)
        self.save()


class Jogador(models.Model):
    id_jogador = models.AutoField(primary_key=True)
    nome_jogador = models.CharField(max_length=100)
    cor_jogador = models.CharField(max_length=50)
    id_partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    id_baralho = models.IntegerField(null=True, blank=True)
    id_casa = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome_jogador


class Baralho(models.Model):
    id_baralho = models.AutoField(primary_key=True)
    id_partida = models.ForeignKey('Partida', on_delete=models.CASCADE) 
    id_jogador = models.OneToOneField('Jogador', on_delete=models.CASCADE, null=True, blank=True)  
    lista_de_cartas = models.TextField(null=True, blank=True) 



class BaralhoCadastro(models.Model):
    id_carta = models.AutoField(primary_key=True)
    nome_carta = models.CharField(max_length=100)
    tipo_carta = models.CharField(max_length=50)
    cor_carta = models.CharField(max_length=50)
    descricao_carta = models.TextField()


class TabuleiroCadastro(models.Model):
    id_casa = models.AutoField(primary_key=True)
    nome_casa = models.CharField(max_length=100)
    acao = models.CharField(max_length=100)


class AcaoCadastro(models.Model):
    id_acao = models.AutoField(primary_key=True)
    nome_acao = models.CharField(max_length=100)

