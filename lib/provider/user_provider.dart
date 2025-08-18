// ignore_for_file: unused_local_variable, prefer_const_declarations, non_constant_identifier_names, avoid_print

import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/model/game_request_model.dart';
import 'package:nb_game/model/user_model_api.dart';
import 'package:nb_game/storage/storage_preferences.dart';
import 'package:shared_preferences/shared_preferences.dart';

final userAndDeckProvider = FutureProvider<GameResponse>(
  (ref) async {
    final localStorageService = LocalStorageService();

    final String? userId = await localStorageService.retrieveUserId();
    //final url = Uri.parse('https://nb-game-mja.wn.r.appspot.com/users/$userId');
    final url = Uri.parse('http://127.0.0.1:8080/users/$userId');
    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final jsonData = json.decode(utf8.decode(response.bodyBytes));
      return GameResponse.fromJson(jsonData);
    } else {
      throw Exception('Falha ao carregar dados: ${response.body}');
    }
  },
);

Future<void> sendGameData({
  required String roundId,
  required String userId,
  required int diceNumber,
  required List<dynamic> choices,
  required bool wantOut,
}) async {
  final url = Uri.parse('http://127.0.0.1:8080/rounds/play'); // ajuste para seu endpoint correto

  final request = GameRequest(
    roundId: roundId,
    userId: userId,
    choices: choices,
    diceNumber: diceNumber,
    wantOut: wantOut,
  );

  final response = await http.post(
    url,
    headers: {
      'Content-Type': 'application/json',
    },
    body: json.encode(request.toJson()),
  );

  if (response.statusCode == 200) {
    print("Dados enviados com sucesso: ${response.body}");
  } else {
    print("Erro ao enviar dados: ${response.statusCode} - ${response.body}");
    throw Exception("Erro ao enviar dados");
  }
}
