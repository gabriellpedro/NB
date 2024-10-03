// ignore_for_file: avoid_print, use_rethrow_when_possible

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

Future<void> postAndStoreData(
  BuildContext context, {
  required String name,
  required String gamePin,
  required String birthDate,
  String? roundId,
}) async {
  try {
    // final url = Uri.parse('http://127.0.0.1:8080/users/');
    final url = Uri.parse('https://nb-game-mja.wn.r.appspot.com/users/');

    final Map<String, dynamic> bodyData = {
      'name': name, // Campo obrigatório
      'game_pin': gamePin, // Campo obrigatório
      'birth_date': birthDate, // Campo obrigatório
      'round_id': roundId, // Campo opcional
    };

    // Envia a requisição POST
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
      body: json.encode(bodyData),
    );

    // Trata a resposta
    if (response.statusCode == 200) {
      // Sucesso
      final responseData = json.decode(response.body);

      // Salva user_id e round_id no SharedPreferences
      await saveToSharedPreferences(
          responseData['user_id'], responseData['round_id']);

      print('Dados enviados com sucesso: ${response.body}');
    } else {
      throw Exception('Erro: ${response.body}');
    }
  } catch (error) {
    // Captura de exceções
    print('Erro ao enviar dados: $error');
    throw error;
  }
}

// Função para salvar user_id e round_id no SharedPreferences
Future<void> saveToSharedPreferences(String userId, String? roundId) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString(
    'user_id',
    userId,
  );
  if (roundId != null) {
    await prefs.setString(
      'round_id',
      roundId,
    );
  }
}
