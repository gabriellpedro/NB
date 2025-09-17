import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

final notificacoesProvider = FutureProvider.autoDispose.family<List<Map<String, dynamic>>, int>((ref, jogadorId) async {
  final jogador = await ref.read(jogadorProvider.future);

  final response = await http.get(
    Uri.parse(
      "http://127.0.0.1:8000/notificacoes/jogador/${jogador.idJogador}/partida/${jogador.idPartida}/",
    ),
  );

  if (response.statusCode != 200) return [];
  final jsonResp = jsonDecode(utf8.decode(response.bodyBytes));
  return List<Map<String, dynamic>>.from(jsonResp["pendentes"]);
});
