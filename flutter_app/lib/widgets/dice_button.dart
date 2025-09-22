// ignore_for_file: unused_local_variable, unused_result, use_build_context_synchronously

import 'dart:math';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';

class DiceButton extends ConsumerWidget {
  const DiceButton({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return SizedBox(
      width: 125,
      height: 125,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.all(1),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        ),
        onPressed: () async {
          final jogadorAsync = ref.read(jogadorProvider.future);
          final jogador = await jogadorAsync;

          final random = Random();
          final result = random.nextInt(6) + 1;

          // Popup 1: resultado do dado
          await showDialog(
            context: context,
            builder: (_) => Dialog(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text("Você tirou: $result",
                        style: const TextStyle(
                            fontSize: 22, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 20),
                    ElevatedButton(
                        onPressed: () => Navigator.of(context).pop(),
                        child: const Text("Ok")),
                  ],
                ),
              ),
            ),
          );

          // POST para rolar o dado e atualizar posição
          final response = await http.post(
            Uri.parse('http://127.0.0.1:8000/rolar-dado/'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(
                {'id_jogador': jogador.idJogador, 'valor_dado': result}),
          );

          if (response.statusCode == 200) {
            final jsonResp = jsonDecode(utf8.decode(response.bodyBytes));
            final novaPosicao = jsonResp['nova_posicao'];
            final idCasa = novaPosicao['id_casa'];
            final idAcao = novaPosicao['id_acao'];

            // Atualiza jogador localmente
            ref.refresh(jogadorProvider); // Atualiza tela

            // Popup 2: Nome da casa
            await showDialog(
              context: context,
              builder: (_) => Dialog(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16)),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(novaPosicao['nome_casa'] ?? 'Nenhuma ação',
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontSize: 20)),
                      const SizedBox(height: 20),
                      ElevatedButton(
                          onPressed: () => Navigator.of(context).pop(),
                          child: const Text("Ok")),
                    ],
                  ),
                ),
              ),
            );

            // Ações que envolvem distribuição/remoção/troca de cartas
            if (idAcao != null &&
                [2, 3, 4, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17, 23, 24, 25]
                    .contains(idAcao)) {
              String? tipoCartaSelecionada;

              // Popup especial para ação 5
              if (idAcao == 5) {
                tipoCartaSelecionada = await showDialog<String>(
                  context: context,
                  builder: (_) => Dialog(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Text(
                            "Escolha o tipo de carta que deseja receber:",
                            style: TextStyle(fontSize: 18),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 20),
                          ElevatedButton(
                            onPressed: () =>
                                Navigator.of(context).pop("inicio"),
                            child: const Text("Início"),
                          ),
                          const SizedBox(height: 20),
                          ElevatedButton(
                            onPressed: () => Navigator.of(context).pop("meio"),
                            child: const Text("Meio"),
                          ),
                          const SizedBox(height: 20),
                          ElevatedButton(
                            onPressed: () => Navigator.of(context).pop("final"),
                            child: const Text("Final"),
                          ),
                        ],
                      ),
                    ),
                  ),
                );

                // Se o usuário fechar sem escolher
                if (tipoCartaSelecionada == null) return;
              }

              // Chama a API passando o tipo da carta apenas se idAcao == 5
              final acaoBody = {
                'id_jogador': jogador.idJogador,
                'id_casa': idCasa,
                if (idAcao == 5) 'tipo_carta': tipoCartaSelecionada,
              };

              final acaoResponse = await http.post(
                Uri.parse('http://127.0.0.1:8000/executar-acao-casa/'),
                headers: {'Content-Type': 'application/json'},
                body: jsonEncode(acaoBody),
              );

              if (acaoResponse.statusCode == 200) {
                final acaoJson =
                    jsonDecode(utf8.decode(acaoResponse.bodyBytes));

                final String mensagem =
                    acaoJson['mensagem'] ?? "Ação concluída";

                final List<dynamic> cartasAdicionadas =
                    acaoJson['cartas_adicionadas'] ?? [];
                final List<dynamic> cartasRemovidas =
                    acaoJson['cartas_removidas'] ?? [];

                // Sempre mostra popup se houver mensagem ou cartas
                if (mensagem.isNotEmpty ||
                    cartasAdicionadas.isNotEmpty ||
                    cartasRemovidas.isNotEmpty) {
                  await showDialog(
                    context: context,
                    builder: (_) => Dialog(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text(
                              "Ação concluída",
                              style: TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.bold,
                              ),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 20),
                            if (idCasa != 20 && idCasa != 25) ...[
                              if (mensagem.isNotEmpty)
                                Text(
                                  mensagem,
                                  style: const TextStyle(fontSize: 18),
                                  textAlign: TextAlign.center,
                                ),
                              const SizedBox(height: 20),
                              if (cartasAdicionadas.isNotEmpty ||
                                  cartasRemovidas.isNotEmpty)
                                ConstrainedBox(
                                  constraints:
                                      const BoxConstraints(maxHeight: 300),
                                  child: ListView(
                                    shrinkWrap: true,
                                    children: [
                                      if (cartasAdicionadas.isNotEmpty)
                                        ...cartasAdicionadas.map(
                                          (carta) => ListTile(
                                            leading: const Icon(Icons.add,
                                                color: Colors.green),
                                            title: Text(carta['nome']),
                                            subtitle:
                                                const Text("Carta recebida"),
                                          ),
                                        ),
                                      if (cartasRemovidas.isNotEmpty)
                                        ...cartasRemovidas.map(
                                          (carta) => ListTile(
                                            leading: const Icon(Icons.remove,
                                                color: Colors.red),
                                            title: Text(carta['nome']),
                                            subtitle:
                                                const Text("Carta perdida"),
                                          ),
                                        ),
                                    ],
                                  ),
                                ),
                            ],
                            const SizedBox(height: 20),
                            ElevatedButton(
                              onPressed: () => Navigator.of(context).pop(),
                              child: const Text("Ok"),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }

                // Atualiza jogador após ação
                ref.refresh(jogadorProvider);
              }
            }
          }
        },
        child: Image.asset('assets/images/dice.png', fit: BoxFit.cover),
      ),
    );
  }
}
