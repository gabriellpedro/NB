// ignore_for_file: prefer_const_constructors, use_build_context_synchronously, unused_result

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

class ButtonDiscard extends ConsumerStatefulWidget {
  const ButtonDiscard({super.key});

  @override
  ConsumerState<ButtonDiscard> createState() => _ButtonDiscardState();
}

class _ButtonDiscardState extends ConsumerState<ButtonDiscard> {
  String? selectedCardId;
  List<Map<String, dynamic>> cartas = [];

  // ============================
  // GET CARTAS DO JOGADOR
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
                'descricao_carta': c['descricao_carta'] ?? "",
              })
          .toList();
    }
    return [];
  }

  // ============================
  // DESCARTAR CARTA
  // ============================
  Future<void> _descartarCarta(int idJogador, int idCarta) async {
    final response = await http.post(
      Uri.parse(
          'http://127.0.0.1:8000/jogador/$idJogador/descartar-carta/$idCarta/'),
      headers: {"Content-Type": "application/json"},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      final mensagem = data['mensagem'] ?? "Carta descartada com sucesso!";
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(mensagem)));
      ref.refresh(jogadorProvider);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erro ao descartar carta.")),
      );
    }
  }

  // ============================
  // POPUP DE SELEÇÃO DE CARTA
  // ============================
  Future<void> _openCardSelectionDialog(
      BuildContext context, int jogadorId) async {
    cartas = await _getCartasJogador(jogadorId);
    selectedCardId = null;

    if (cartas.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Você não possui cartas.")),
      );
      return;
    }

    if (!mounted) return;

    showDialog(
      context: context,
      builder: (_) => StatefulBuilder(
        builder: (context, setStateDialog) {
          return AlertDialog(
            title: const Text("Selecione uma carta para descartar"),
            content: SizedBox(
              width: double.maxFinite,
              height: 300,
              child: ListView.builder(
                itemCount: cartas.length,
                itemBuilder: (context, index) {
                  final carta = cartas[index];
                  return ListTile(
                    title: Text(carta['nome_carta']),
                    subtitle: Text(
                      carta['descricao_carta'],
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
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
                        await _descartarCarta(
                            jogadorId, int.parse(selectedCardId!));
                        Navigator.of(context).pop();
                      }
                    : null,
                child: const Text("Confirmar"),
              ),
            ],
          );
        },
      ),
    );
  }

  // ============================
  // BOTÃO PRINCIPAL
  // ============================
  void _onPressedButton(BuildContext context) async {
    final jogadorAsync = ref.watch(jogadorProvider);

    jogadorAsync.when(
      data: (jogador) async {
        await _openCardSelectionDialog(context, jogador.idJogador);
      },
      loading: () => print("Carregando jogador..."),
      error: (err, _) => print("Erro ao carregar jogador: $err"),
    );
  }

  // ============================
  // BUILD
  // ============================
  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Descartar Carta',
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
            'assets/images/descarte_carta.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
