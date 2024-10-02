// ignore_for_file: unused_local_variable, prefer_const_declarations, non_constant_identifier_names, avoid_print

import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/model/user_model_api.dart';

final userAndDeckProvider = FutureProvider<GameResponse>(
  (ref) async {
    final String userId = 'aSfwEF17TCslSXs38T2K';
    final url = Uri.parse('http://10.0.2.2:5000/users/$userId');

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
