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

class Jogador {
  final int idPartida;
  final int idJogador;
  final String nomeJogador;
  final String corJogador;
  final int? idCasa;
  final String? nomeCasa;
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

  Jogador copyWith({
    int? idPartida,
    int? idJogador,
    String? nomeJogador,
    String? corJogador,
    int? idCasa,
    String? nomeCasa,
    List<Carta>? cartas,
  }) {
    return Jogador(
      idPartida: idPartida ?? this.idPartida,
      idJogador: idJogador ?? this.idJogador,
      nomeJogador: nomeJogador ?? this.nomeJogador,
      corJogador: corJogador ?? this.corJogador,
      idCasa: idCasa ?? this.idCasa,
      nomeCasa: nomeCasa ?? this.nomeCasa,
      cartas: cartas ?? this.cartas,
    );
  }
}
