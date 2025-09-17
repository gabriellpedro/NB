// ignore_for_file: unused_local_variable, use_build_context_synchronously, unused_result

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

class ButtonDonate extends ConsumerWidget {
  const ButtonDonate({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Tooltip(
      message: 'Doar carta',
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
            final jogadorAsync = ref.read(jogadorProvider.future);
            final jogador = await jogadorAsync;

            final idCasa = jogador.idCasa;
            if (idCasa == null) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Jogador não está em uma casa válida.")),
              );
              return;
            }

            // Buscar cartas do jogador
            final cartasResponse = await http.get(
              Uri.parse('http://127.0.0.1:8000/jogador/${jogador.idJogador}/cartas'),
            );
            if (cartasResponse.statusCode != 200) return;

            final cartasJson = jsonDecode(utf8.decode(cartasResponse.bodyBytes));
            final List cartas = cartasJson['cartas'] ?? [];

            if (cartas.isEmpty) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Você não possui cartas para doar.")),
              );
              return;
            }

            // Popup: Seleção da carta
            Map? cartaSelecionada;
            await showDialog(
              context: context,
              builder: (_) => AlertDialog(
                title: const Text("Selecione uma carta para doar"),
                content: SizedBox(
                  width: double.maxFinite,
                  height: 300,
                  child: ListView.builder(
                    shrinkWrap: true,
                    itemCount: cartas.length,
                    itemBuilder: (context, index) {
                      final carta = cartas[index];
                      return ListTile(
                        title: Text(carta['nome_carta']),
                        subtitle: Text(carta['descricao_carta'] ?? ""),
                        onTap: () {
                          cartaSelecionada = carta;
                          Navigator.of(context).pop();
                        },
                      );
                    },
                  ),
                ),
              ),
            );

            if (cartaSelecionada == null) return;

            // Popup: Seleção do jogador destino
            final jogadoresResponse = await http.get(
              Uri.parse('http://127.0.0.1:8000/partida/${jogador.idPartida}/jogadores/'),
            );
            if (jogadoresResponse.statusCode != 200) return;

            final jogadoresJson = jsonDecode(utf8.decode(jogadoresResponse.bodyBytes));
            final List jogadores = jogadoresJson['jogadores'] ?? [];

            // Remove o jogador atual da lista
            jogadores.removeWhere((j) => j['id_jogador'] == jogador.idJogador);

            Map? jogadorDestino;
            await showDialog(
              context: context,
              builder: (_) => AlertDialog(
                title: const Text("Selecione o jogador destino"),
                content: SizedBox(
                  width: double.maxFinite,
                  height: 300,
                  child: ListView.builder(
                    shrinkWrap: true,
                    itemCount: jogadores.length,
                    itemBuilder: (context, index) {
                      final j = jogadores[index];
                      return ListTile(
                        title: Text(j['nome_jogador']),
                        onTap: () {
                          jogadorDestino = j;
                          Navigator.of(context).pop();
                        },
                      );
                    },
                  ),
                ),
              ),
            );

            if (jogadorDestino == null) return;

            // Chama endpoint executar-acao-casa/
            final donateResponse = await http.post(
              Uri.parse('http://127.0.0.1:8000/executar-acao-casa/'),
              headers: {'Content-Type': 'application/json'},
              body: jsonEncode({
                'id_jogador': jogador.idJogador,
                'id_casa': idCasa,
                'id_jogador_destino': jogadorDestino?['id_jogador'],
                'id_carta': cartaSelecionada?['id_carta'],
              }),
            );

            if (donateResponse.statusCode == 200) {
              final jsonResp = jsonDecode(utf8.decode(donateResponse.bodyBytes));
              final mensagem = jsonResp['mensagem'] ?? "Carta doada com sucesso";

              // Atualiza o jogador (e UI)
              ref.refresh(jogadorProvider);

              // Feedback visual
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(mensagem)),
              );
            }
          },
          child: Image.asset(
            'assets/images/pegar_carta.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
