// ignore_for_file: prefer_const_constructors, avoid_print, sort_child_properties_last, use_build_context_synchronously, unused_result

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

class PlayerSelectionButton extends ConsumerStatefulWidget {
  const PlayerSelectionButton({super.key});

  @override
  ConsumerState<PlayerSelectionButton> createState() =>
      _PlayerSelectionButtonState();
}

class _PlayerSelectionButtonState extends ConsumerState<PlayerSelectionButton> {
  String? selectedCardId;
  List<Map<String, dynamic>> cartas = [];

  // ============================
  // GET JOGADOR À ESQUERDA
  // ============================
  Future<Map<String, dynamic>?> _getJogadorEsquerda(int jogadorId) async {
    final response = await http
        .get(Uri.parse('http://127.0.0.1:8000/jogador/$jogadorId/esquerda/'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return {
        "id": data['id_jogador_esquerda'],
        "nome": data['nome_jogador_esquerda'],
      };
    }
    return null;
  }

  // ============================
  // GET JOGADOR À DIREITA
  // ============================
  Future<Map<String, dynamic>?> _getJogadorDireita(int jogadorId) async {
    final response = await http
        .get(Uri.parse('http://127.0.0.1:8000/jogador/$jogadorId/direita/'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return {
        "id": data['id_jogador_direita'],
        "nome": data['nome_jogador_direita'],
      };
    }
    return null;
  }

  // ============================
  // GET JOGADORES DA PARTIDA
  // ============================
  Future<List<Map<String, dynamic>>> _getJogadoresPartida(
      int idPartida, int idJogadorAtual) async {
    final response = await http
        .get(Uri.parse('http://127.0.0.1:8000/partida/$idPartida/jogadores/'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final List jogadores = data['jogadores'] ?? [];
      // Exclui o jogador atual
      return jogadores
          .where((j) => j['id_jogador'] != idJogadorAtual)
          .map<Map<String, dynamic>>((j) => {
                'id': j['id_jogador'],
                'nome': j['nome_jogador'],
              })
          .toList();
    }
    return [];
  }

  // ============================
  // GET CARTAS
  // ============================
  Future<List<Map<String, dynamic>>> _getCartasJogador(int jogadorId) async {
    final response = await http
        .get(Uri.parse('http://127.0.0.1:8000/jogador/$jogadorId/cartas'));

    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      final List cartasList = data['cartas'] ?? [];
      return cartasList
          .map<Map<String, dynamic>>((c) => {
                'id_carta': c['id_carta'],
                'nome_carta': c['nome_carta'],
              })
          .toList();
    }
    return [];
  }

  // ============================
  // EXECUTAR AÇÃO
  // ============================
  Future<void> _executarAcaoCasa({
    required int idJogador,
    required int idCasa,
    required int idCarta,
    int? idJogadorDestino,
  }) async {
    final body = jsonEncode({
      "id_jogador": idJogador,
      "id_casa": idCasa,
      "id_carta": idCarta,
      if (idJogadorDestino != null) "id_jogador_destino": idJogadorDestino,
    });

    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/executar-acao-casa/'),
      headers: {"Content-Type": "application/json"},
      body: body,
    );

    if (response.statusCode == 200) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text("Carta roubada!")));
      ref.refresh(jogadorProvider);
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text("Erro ao roubar carta")));
    }
  }

  // ============================
  // POPUP DE SELEÇÃO DE CARTA
  // ============================
  Future<void> _openCardSelectionDialog(
    BuildContext context,
    int jogadorId,
    int idJogadorAtual,
    int idCasa,
    String jogadorNome, {
    int? idJogadorDestino,
  }) async {
    cartas = await _getCartasJogador(jogadorId);
    selectedCardId = null;

    if (cartas.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("$jogadorNome não possui cartas.")),
      );
      return;
    }

    if (!mounted) return;

    showDialog(
      context: context,
      builder: (_) => StatefulBuilder(
        builder: (context, setStateDialog) {
          return AlertDialog(
            title: Text('Escolha uma carta para roubar de $jogadorNome'),
            content: SizedBox(
              width: double.maxFinite,
              height: 300,
              child: ListView.builder(
                itemCount: cartas.length,
                itemBuilder: (context, index) {
                  final carta = cartas[index];
                  return ListTile(
                    title: Text(carta['nome_carta']),
                    leading: Radio<String>(
                      value: carta['id_carta'].toString(),
                      groupValue: selectedCardId,
                      onChanged: (value) {
                        setStateDialog(() {
                          selectedCardId = value;
                        });
                      },
                    ),
                    onTap: () {
                      setStateDialog(() {
                        selectedCardId = carta['id_carta'].toString();
                      });
                    },
                  );
                },
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text("Cancelar"),
              ),
              ElevatedButton(
                onPressed: selectedCardId != null
                    ? () async {
                        await _executarAcaoCasa(
                          idJogador: idJogadorAtual,
                          idCasa: idCasa,
                          idCarta: int.parse(selectedCardId!),
                          idJogadorDestino: idJogadorDestino,
                        );
                        Navigator.of(context).pop();
                      }
                    : null,
                child: const Text("OK"),
              ),
            ],
          );
        },
      ),
    );
  }

  // ============================
  // POPUP DE SELEÇÃO DE JOGADOR (CASA 15)
  // ============================
  void _openPlayerSelectionDialog(
    BuildContext context,
    int idPartida,
    int idJogadorAtual,
  ) async {
    final jogadores = await _getJogadoresPartida(idPartida, idJogadorAtual);
    int? selectedJogadorId;
    String? selectedJogadorNome;

    if (jogadores.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Nenhum jogador disponível.")),
      );
      return;
    }

    if (!mounted) return;

    showDialog(
      context: context,
      builder: (_) => StatefulBuilder(
        builder: (context, setStateDialog) {
          return AlertDialog(
            title: const Text('Escolha o jogador que deseja roubar'),
            content: SizedBox(
              width: double.maxFinite,
              height: 300,
              child: ListView.builder(
                itemCount: jogadores.length,
                itemBuilder: (context, index) {
                  final jogador = jogadores[index];
                  return ListTile(
                    title: Text(jogador['nome']),
                    leading: Radio<int>(
                      value: jogador['id'],
                      groupValue: selectedJogadorId,
                      onChanged: (value) {
                        setStateDialog(() {
                          selectedJogadorId = value;
                          selectedJogadorNome = jogador['nome'];
                        });
                      },
                    ),
                    onTap: () {
                      setStateDialog(() {
                        selectedJogadorId = jogador['id'];
                        selectedJogadorNome = jogador['nome'];
                      });
                    },
                  );
                },
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text("Cancelar"),
              ),
              ElevatedButton(
                onPressed: selectedJogadorId != null
                    ? () {
                        Navigator.of(context).pop();
                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          _openCardSelectionDialog(
                            context,
                            selectedJogadorId!,
                            idJogadorAtual,
                            15,
                            selectedJogadorNome!,
                            idJogadorDestino: selectedJogadorId,
                          );
                        });
                      }
                    : null,
                child: const Text("OK"),
              ),
            ],
          );
        },
      ),
    );
  }

  // ============================
  // BOTÃO ÚNICO
  // ============================
  void _onPressedButton(BuildContext context) async {
    final jogadorAsync = ref.watch(jogadorProvider);

    jogadorAsync.when(
      data: (jogador) async {
        final idCasa = jogador.idCasa!;
        Map<String, dynamic>? jogadorAlvo;

        if (idCasa == 11) {
          jogadorAlvo = await _getJogadorEsquerda(jogador.idJogador);
        } else if (idCasa == 29) {
          jogadorAlvo = await _getJogadorDireita(jogador.idJogador);
        } else if (idCasa == 15) {
          _openPlayerSelectionDialog(
              context, jogador.idPartida!, jogador.idJogador);
          return;
        } else {
          return;
        }

        if (jogadorAlvo == null) return;

        _openCardSelectionDialog(
          context,
          jogadorAlvo["id"],
          jogador.idJogador,
          idCasa,
          jogadorAlvo["nome"],
        );
      },
      loading: () => print("Carregando..."),
      error: (err, _) => print("Erro: $err"),
    );
  }

  // ============================
  // BUILD
  // ============================
  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Escolher jogador para visualizar o baralho',
      child: SizedBox(
        width: 125,
        height: 125,
        child: ElevatedButton(
          onPressed: () => _onPressedButton(context),
          style: ElevatedButton.styleFrom(
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            padding: const EdgeInsets.all(1),
          ),
          child: Image.asset(
            'assets/images/ver_baralho.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
