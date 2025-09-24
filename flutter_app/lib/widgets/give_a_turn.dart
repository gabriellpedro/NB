// ignore_for_file: use_build_context_synchronously, unused_result

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

/// ---------------------------
/// API CALLS
/// ---------------------------

Future<List<Map<String, dynamic>>> fetchJogadores(int idPartida) async {
  final response = await http.get(
    Uri.parse("http://127.0.0.1:8000/partida/$idPartida/jogadores/"),
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);

    // espera um mapa com chave "jogadores"
    if (data is Map<String, dynamic> && data.containsKey("jogadores")) {
      return (data["jogadores"] as List)
          .map((j) => Map<String, dynamic>.from(j as Map))
          .toList();
    }

    throw Exception("Formato inesperado de resposta: $data");
  } else {
    throw Exception("Erro ao carregar jogadores (status ${response.statusCode})");
  }
}

Future<void> atualizarControleJogador({
  required int idPartida,
  required int idJogador,
  required int idGravacao,
  required int valor,
}) async {
  final response = await http.post(
    Uri.parse("http://127.0.0.1:8000/atualizar-controle-jogador/"),
    headers: {"Content-Type": "application/json"},
    body: json.encode({
      "id_partida": idPartida,
      "id_jogador": idJogador,
      "id_gravacao": idGravacao,
      "valor": valor,
    }),
  );

  if (response.statusCode != 200) {
    throw Exception("Erro ao atualizar jogador: ${response.body}");
  }
}

/// ---------------------------
/// WIDGET
/// ---------------------------

class SelecaoJogadorButton extends ConsumerWidget {
  const SelecaoJogadorButton({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Tooltip(
      message: 'Escolher jogador ceder a vez',
      child: SizedBox(
        width: 125,
        height: 125,
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.all(1),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          onPressed: () async {
            // pega jogador atual (origem) via provider
            final jogador = await ref.read(jogadorProvider.future);

            try {
              // carrega jogadores da partida
              final todos = await fetchJogadores(jogador.idPartida);

              // filtra para não incluir o próprio jogador
              final jogadores = todos
                  .where((j) => j['id_jogador'] != jogador.idJogador)
                  .toList();

              if (jogadores.isEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Não há outros jogadores na partida.")),
                );
                return;
              }

              // abre diálogo de seleção e aguarda o jogador selecionado como retorno
              final Map<String, dynamic>? selecionado =
                  await showDialog<Map<String, dynamic>>(
                context: context,
                builder: (dialogContext) {
                  Map<String, dynamic>? temp = jogadores.first;
                  return StatefulBuilder(
                    builder: (ctx, setState) {
                      return AlertDialog(
                        title: const Text('Escolha o jogador'),
                        content: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            DropdownButtonFormField<Map<String, dynamic>>(
                              value: temp,
                              items: jogadores
                                  .map((j) => DropdownMenuItem(
                                        value: j,
                                        child: Text(j["nome_jogador"] ?? "Sem nome"),
                                      ))
                                  .toList(),
                              onChanged: (value) {
                                setState(() {
                                  temp = value;
                                });
                              },
                              decoration: const InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                            ),
                          ],
                        ),
                        actions: [
                          TextButton(
                            onPressed: () {
                              // fecha dialog sem retornar seleção
                              Navigator.of(dialogContext).pop(null);
                            },
                            child: const Text('Cancelar'),
                          ),
                          ElevatedButton(
                            onPressed: temp == null
                                ? null
                                : () {
                                    // fecha e retorna o jogador selecionado
                                    Navigator.of(dialogContext).pop(temp);
                                  },
                            child: const Text('Confirmar'),
                          ),
                        ],
                      );
                    },
                  );
                },
              );

              // se o usuário fechou sem selecionar
              if (selecionado == null) return;

              // executa as duas atualizações na API:
              // 1) destino ganha vez extra (id_gravacao = 2, valor = 1)
              // 2) origem perde a vez (id_gravacao = 1, valor = 1)
              try {
                await atualizarControleJogador(
                  idPartida: jogador.idPartida,
                  idJogador: selecionado["id_jogador"],
                  idGravacao: 2,
                  valor: 1,
                );

                await atualizarControleJogador(
                  idPartida: jogador.idPartida,
                  idJogador: jogador.idJogador,
                  idGravacao: 1,
                  valor: 1,
                );
              } catch (e) {
                // se falhar ao atualizar, informa e retorna
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text("Erro ao atualizar controle: $e")),
                );
                return;
              }

              // mostra popup simples de confirmação (usa successContext para pop correto)
              await showDialog(
                context: context,
                builder: (successContext) => AlertDialog(
                  title: const Text("Sucesso"),
                  content: const Text("Vez doada com sucesso!"),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.of(successContext).pop(),
                      child: const Text("OK"),
                    ),
                  ],
                ),
              );

              // atualiza provider para refletir mudanças
              ref.refresh(jogadorProvider);
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text("Erro ao carregar jogadores: $e")),
              );
            }
          },
          child: Image.asset(
            'assets/images/turno.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
