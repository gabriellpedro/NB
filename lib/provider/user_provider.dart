// ignore_for_file: unused_local_variable

import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/model/user_model.dart';

final userProvider = FutureProvider<User>((ref) async {
  final String user_id = '523xUj3jNQWkuoiijSt3'; // Substitua pelo ID apropriado
  final url = Uri.parse('http://10.0.2.2:5000/users/$user_id');
  // final url = Uri.parse('http://127.0.0.1:5000/users/1');

  final response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
    },
  );

  if (response.statusCode == 200) {
    final jsonData = json.decode(utf8.decode(response.bodyBytes));

    print(response.body);

    if (jsonData['user'] != null) {
      return User.fromJson(Map<String, dynamic>.from(jsonData['user']));
    } else {
      throw Exception('Usuário não encontrado');
    }
  } else {
    throw Exception('Falha ao carregar usuário: ${response.body}');
  }
});
