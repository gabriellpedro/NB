import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> marcarNotificacaoProcessada(int id) async {
  final response = await http.post(
    Uri.parse("http://127.0.0.1:8000/notificacoes/processar/"),
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"id_notificacao": id}),
  );

  if (response.statusCode != 200) {
    throw Exception("Erro ao processar notificação: ${response.body}");
  }
}
