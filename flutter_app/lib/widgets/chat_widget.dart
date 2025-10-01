// ignore_for_file: use_build_context_synchronously, unused_result

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

class ChatButton extends ConsumerStatefulWidget {
  const ChatButton({super.key});

  @override
  ConsumerState<ChatButton> createState() => _ChatButtonState();
}

class _ChatButtonState extends ConsumerState<ChatButton> {
  final TextEditingController _controller = TextEditingController();
  String? _selectedUserId;
  List<Map<String, dynamic>> _players = [];
  List<Map<String, dynamic>> _elogios = [];

  Future<void> _fetchPlayers(int idPartida, int idJogadorAtual) async {
    final response = await http.get(
      Uri.parse("http://127.0.0.1:8000/partida/$idPartida/jogadores/"),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List jogadores = data["jogadores"] ?? [];
      setState(() {
        _players = jogadores
            .where((j) => j['id_jogador'] != idJogadorAtual)
            .map<Map<String, dynamic>>((j) => {
                  "id_jogador": j["id_jogador"],
                  "nome_jogador": j["nome_jogador"]
                })
            .toList();
        if (_players.isNotEmpty) {
          _selectedUserId ??= _players.first["id_jogador"].toString();
        }
      });
    }
  }

  Future<void> _fetchElogios(int idPartida) async {
    final response = await http.get(
      Uri.parse("http://127.0.0.1:8000/partida/$idPartida/elogios/"),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List elogios = data["elogios"] ?? [];
      setState(() {
        _elogios = elogios
            .map<Map<String, dynamic>>((e) => {
                  "origem": e["origem"],
                  "destino": e["destino"],
                  "mensagem": e["mensagem"]
                })
            .toList();
      });
    }
  }

  Future<void> _sendElogio(int idJogadorOrigem, int idJogadorDestino) async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    final response = await http.post(
      Uri.parse("http://127.0.0.1:8000/criar-elogio/"),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        "jogador_origem": idJogadorOrigem,
        "jogador_destino": idJogadorDestino,
        "mensagem": text,
      }),
    );

    if (response.statusCode == 200) {
      _controller.clear();
      await _fetchElogios(idJogadorOrigem); // atualiza a lista
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Elogio enviado com sucesso!")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erro ao enviar elogio.")),
      );
    }
  }

  void _showChatPopup(BuildContext context) async {
    final jogador = await ref.read(jogadorProvider.future);
    final idJogadorAtual = jogador.idJogador;
    final idPartida = jogador.idPartida;

    await _fetchPlayers(idPartida, idJogadorAtual);
    await _fetchElogios(idPartida);

    showDialog(
      context: context,
      builder: (_) {
        return Dialog(
          insetPadding: const EdgeInsets.all(40),
          child: Container(
            width: 350,
            height: 500,
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                const Text(
                  'Enviar Elogio',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      children: _elogios.map((e) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 6.0),
                          child: Container(
                            width: double.infinity,
                            decoration: BoxDecoration(
                              border: Border.all(color: Colors.grey.shade300),
                              borderRadius: BorderRadius.circular(6),
                              color: Colors.grey.shade100,
                            ),
                            padding: const EdgeInsets.all(8),
                            child: Text(
                              "De: ${e['origem']}\nPara: ${e['destino']}\nMensagem: ${e['mensagem']}",
                              style: const TextStyle(fontSize: 14),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ),
                const Divider(),
                TextField(
                  controller: _controller,
                  maxLines: 3,
                  decoration: const InputDecoration(
                    hintText: 'Digite seu elogio',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 8),
                DropdownButtonFormField<String>(
                  value: _selectedUserId,
                  hint: const Text('Selecione o destinatário'),
                  onChanged: (value) {
                    setState(() {
                      _selectedUserId = value;
                    });
                  },
                  items: _players.map((j) {
                    return DropdownMenuItem<String>(
                      value: j["id_jogador"].toString(),
                      child: Text(j["nome_jogador"] ?? "Sem nome"),
                    );
                  }).toList(),
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    contentPadding: EdgeInsets.symmetric(horizontal: 12),
                  ),
                ),
                const SizedBox(height: 8),
                ElevatedButton(
                  onPressed: _selectedUserId == null
                      ? null
                      : () => _sendElogio(
                            idJogadorAtual,
                            int.parse(_selectedUserId!),
                          ),
                  child: const Text("Enviar"),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Enviar elogio',
      child: SizedBox(
        width: 125,
        height: 125,
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.all(1),
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          ),
          onPressed: () => _showChatPopup(context),
          child: Image.asset(
            'assets/images/elogio.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
