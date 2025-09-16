// ignore_for_file: unused_local_variable, non_constant_identifier_names, avoid_print

import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/model/game_request_model.dart';
import 'package:nb_game/provider/user_register.dart';

final jogadorProvider = FutureProvider<Jogador>((ref) async {
  final String? userId = await retrieveUserId();
  if (userId == null || userId.isEmpty) {
    throw Exception('User ID não encontrado no storage');
  }

  final url = Uri.parse('http://127.0.0.1:8000/jogador/$userId/');
  final response = await http.get(
    url,
    headers: {'Content-Type': 'application/json'},
  );

  if (response.statusCode == 200) {
    final jsonData = json.decode(utf8.decode(response.bodyBytes));

    final cartasJson = jsonData['cartas'] as List<dynamic>? ?? [];
    jsonData['cartas'] = cartasJson;

    final returnedUserId = jsonData['id_jogador']?.toString();
    final returnedRoundId = jsonData['id_partida']?.toString();
    if (returnedUserId != null && returnedUserId.isNotEmpty) {
      await saveToSharedPreferences(returnedUserId, returnedRoundId ?? '');
    }

    return Jogador.fromJson(jsonData);
  } else {
    throw Exception('Falha ao carregar dados: ${response.body}');
  }
});

/// Função para rolar dado e atualizar jogador
Future<Jogador> rollDice(FutureProviderRef ref, Jogador jogador) async {
  final valorDado = (1 + (6 * (DateTime.now().millisecondsSinceEpoch % 1000) / 1000)).toInt();

  final response = await http.post(
    Uri.parse('http://127.0.0.1:8000/rolar-dado/'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'id_jogador': jogador.idJogador, 'valor_dado': valorDado}),
  );

  if (response.statusCode == 200) {
    final jsonResp = jsonDecode(response.body);
    final novaPosicao = jsonResp['nova_posicao'];

    return jogador.copyWith(
      idCasa: novaPosicao['id_casa'],
      nomeCasa: novaPosicao['nome_casa'],
    );
  } else {
    throw Exception('Erro ao rolar o dado: ${response.body}');
  }
}
