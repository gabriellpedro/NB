// ignore_for_file: avoid_print, use_rethrow_when_possible

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

// Função para criar jogador e salvar IDs no SharedPreferences
Future<void> postAndStoreData(
  BuildContext context, {
  required String nomeJogador,
  required String corJogador,
  int? idPartida, // opcional
}) async {
  try {
    final url = Uri.parse('http://127.0.0.1:8000/jogador/criar/');

    final Map<String, dynamic> bodyData = {
      'nome_jogador': nomeJogador,
      'cor_jogador': corJogador,
      if (idPartida != null) 'id_partida': idPartida,
    };

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode(bodyData),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      final responseData = json.decode(response.body);

      // Pega o objeto 'jogador' dentro do JSON
      final jogadorData = responseData['jogador'];
      final jogadorId = jogadorData['id_jogador']?.toString() ?? '';
      final partidaId = jogadorData['id_partida']?.toString() ?? '';

      if (jogadorId.isNotEmpty) {
        await saveToSharedPreferences(jogadorId, partidaId);
        print('Dados enviados com sucesso: ${response.body}');
      } else {
        throw Exception('ID do jogador não retornado pela API');
      }
    } else {
      throw Exception('Erro: ${response.body}');
    }
  } catch (error) {
    print('Erro ao enviar dados: $error');
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Falha ao enviar dados: $error')),
    );
    throw error;
  }
}

// Salva user_id e round_id no SharedPreferences
Future<void> saveToSharedPreferences(String userId, String roundId) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('user_id', userId);
  await prefs.setString('round_id', roundId);
}

// Recupera o user_id do SharedPreferences
Future<String?> retrieveUserId() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('user_id');
}

// Recupera o round_id do SharedPreferences
Future<String?> retrieveRoundId() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('round_id');
}

// Remove os IDs do SharedPreferences
Future<void> removeIds() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('user_id');
  await prefs.remove('round_id');
}
