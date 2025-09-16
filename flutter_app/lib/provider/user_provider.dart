// ignore_for_file: unused_local_variable, prefer_const_declarations, non_constant_identifier_names, avoid_print

import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/model/game_request_model.dart'; // Jogador e Carta
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

    // Garante que a lista de cartas nunca seja nula
    final cartasJson = jsonData['cartas'] as List<dynamic>? ?? [];
    jsonData['cartas'] = cartasJson;

    // Atualiza o storage
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
