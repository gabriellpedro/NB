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
    //final url = Uri.parse('http://127.0.0.1:8080/users/');
    final url = Uri.parse('https://nb-game-mja.wn.r.appspot.com/users/');

    String formatRfc1123(DateTime dateTime) {
      final weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      final months = [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'
      ];

      final utc = dateTime.toUtc();
      final weekday = weekdays[utc.weekday - 1];
      final month = months[utc.month - 1];
      final day = utc.day.toString().padLeft(2, '0');
      final hour = utc.hour.toString().padLeft(2, '0');
      final minute = utc.minute.toString().padLeft(2, '0');
      final second = utc.second.toString().padLeft(2, '0');

      return '$weekday, $day $month ${utc.year} $hour:$minute:$second GMT';
    }

    final createdAt = formatRfc1123(
        DateTime.now().toUtc().subtract(const Duration(minutes: 1)));

    final Map<String, dynamic> bodyData = {
      'name': name, // Campo obrigatório
      'game_pin': gamePin, // Campo obrigatório
      'birth_date': birthDate, // Campo obrigatório
      'round_id': roundId, // Campo opcional
      //'created_at': createdAt
    };

    // Envia a requisição POST
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
      body: json.encode(bodyData),
    );

    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);

      // Salva user_id e round_id no SharedPreferences
      await saveToSharedPreferences(
          responseData['user_id'], responseData['round_id']);

      print('Dados enviados com sucesso: ${response.body}');
    } else {
      throw Exception('Erro: ${response.body}');
    }
  } catch (error) {
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
