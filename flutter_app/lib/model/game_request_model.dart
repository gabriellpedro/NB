// Modelo para a Carta
class Carta {
  final int idCarta;
  final String nomeCarta;
  final String tipoCarta;
  final String corCarta;
  final String descricaoCarta;

  Carta({
    required this.idCarta,
    required this.nomeCarta,
    required this.tipoCarta,
    required this.corCarta,
    required this.descricaoCarta,
  });

  factory Carta.fromJson(Map<String, dynamic> json) {
    return Carta(
      idCarta: json['id_carta'],
      nomeCarta: json['nome_carta'],
      tipoCarta: json['tipo_carta'],
      corCarta: json['cor_carta'],
      descricaoCarta: json['descricao_carta'],
    );
  }
}

// Modelo para o Jogador
class Jogador {
  final int idPartida;
  final int idJogador;
  final String nomeJogador;
  final String corJogador;
  final int? idCasa;
  final String? nomeCasa; // Novo campo vindo do backend
  final List<Carta> cartas;

  Jogador({
    required this.idPartida,
    required this.idJogador,
    required this.nomeJogador,
    required this.corJogador,
    this.idCasa,
    this.nomeCasa,
    required this.cartas,
  });

  factory Jogador.fromJson(Map<String, dynamic> json) {
    // Caso 'cartas' seja nulo, cria lista vazia
    var cartasJson = json['cartas'] as List<dynamic>? ?? [];
    List<Carta> cartasList = cartasJson.map((c) => Carta.fromJson(c)).toList();

    return Jogador(
      idPartida: json['id_partida'],
      idJogador: json['id_jogador'],
      nomeJogador: json['nome_jogador'],
      corJogador: json['cor_jogador'],
      idCasa: json['id_casa'],
      nomeCasa: json['nome_casa'], 
      cartas: cartasList,
    );
  }
}
