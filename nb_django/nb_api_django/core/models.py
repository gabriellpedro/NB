import json
from django.db import models


class Partida(models.Model):
    id_partida = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    # Guardando apenas o ID do jogador (Integer ou ObjectId em string)
    id_jogador_amarelo = models.CharField(max_length=24, null=True, blank=True)
    id_jogador_azul = models.CharField(max_length=24, null=True, blank=True)
    id_jogador_preto = models.CharField(max_length=24, null=True, blank=True)
    id_jogador_roxo = models.CharField(max_length=24, null=True, blank=True)

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
    id_partida = models.ForeignKey(
        Partida, on_delete=models.SET_NULL, null=True, blank=True
    )
    id_baralho = models.IntegerField(null=True, blank=True)
    id_casa = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome_jogador


class ControleJogador(models.Model):
    id_controle_jogador = models.AutoField(primary_key=True)
    id_partida = models.ForeignKey(
        "Partida", on_delete=models.CASCADE, related_name="controles_jogadores"
    )
    id_jogador = models.ForeignKey(
        "Jogador", on_delete=models.CASCADE, related_name="controles"
    )

    # Número de rodadas que o jogador deve ficar sem jogar
    sem_jogar_rodadas = models.IntegerField(default=0)

    # Número de vezes extras que o jogador terá para jogar em sua rodada
    vezes_extra = models.IntegerField(default=0)

    atualizado_em = models.DateTimeField(auto_now=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("id_partida", "id_jogador")
        verbose_name = "Controle de Jogador"
        verbose_name_plural = "Controles de Jogadores"

    def __str__(self):
        return f"ControleJogador - Partida {self.id_partida.id_partida}, Jogador {self.id_jogador.id_jogador}"


class Baralho(models.Model):
    id_baralho = models.AutoField(primary_key=True)
    id_partida = models.ForeignKey("Partida", on_delete=models.CASCADE)
    id_jogador = models.OneToOneField(
        "Jogador", on_delete=models.SET_NULL, null=True, blank=True
    )
    lista_de_cartas = models.TextField(null=True, blank=True)


class BaralhoCadastro(models.Model):
    id_carta = models.AutoField(primary_key=True)
    nome_carta = models.CharField(max_length=100)
    tipo_carta = models.CharField(max_length=50)
    cor_carta = models.CharField(max_length=50)
    descricao_carta = models.TextField()


class AcaoCadastro(models.Model):
    id_acao = models.AutoField(primary_key=True)
    nome_acao = models.CharField(max_length=100)  # Nome curto
    tipo_carta = models.CharField(
        max_length=10, null=True, blank=True
    )  # INICIO, MEIO, FIM
    descricao = models.TextField(null=True, blank=True)  # Texto mais detalhado

    def __str__(self):
        return self.nome_acao


class TabuleiroCadastro(models.Model):
    id_casa = models.AutoField(primary_key=True)
    numero_casa = models.IntegerField(unique=True)  # Casa 1, 2, 3...
    nome_casa = models.CharField(max_length=100)  # Ex: "Início", "Ganhe 1 carta de FIM"
    acao = models.ForeignKey(
        AcaoCadastro, on_delete=models.CASCADE, related_name="casas"
    )

    def __str__(self):
        return f"Casa {self.numero_casa} - {self.nome_casa}"


class Elogio(models.Model):
    id_elogio = models.AutoField(primary_key=True)
    id_partida = models.ForeignKey(
        Partida, on_delete=models.CASCADE, related_name="elogios"
    )
    jogador_origem = models.ForeignKey(
        Jogador, on_delete=models.CASCADE, related_name="elogios_enviados"
    )
    jogador_destino = models.ForeignKey(
        Jogador, on_delete=models.CASCADE, related_name="elogios_recebidos"
    )
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Elogio de {self.jogador_origem.nome_jogador} para {self.jogador_destino.nome_jogador} na Partida {self.id_partida.id_partida}"


class Notificacao(models.Model):
    id_notificacao = models.AutoField(primary_key=True)
    id_jogador_origem = models.ForeignKey(
        "Jogador", on_delete=models.CASCADE, related_name="notificacoes_enviadas"
    )
    id_jogador_destino = models.ForeignKey(
        "Jogador", on_delete=models.CASCADE, related_name="notificacoes_recebidas"
    )
    id_partida = models.IntegerField()  # Apenas controle numérico
    mensagem = models.TextField()
    necessita_atualizar = models.BooleanField(default=True)
    processado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação {self.id_notificacao} (Partida {self.id_partida})"
