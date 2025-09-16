import 'dart:math';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/model/game_request_model.dart';

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

          await showDialog(
            context: context,
            builder: (_) => Dialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text("Você tirou: $result", style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 20),
                    ElevatedButton(onPressed: () => Navigator.of(context).pop(), child: const Text("Ok")),
                  ],
                ),
              ),
            ),
          );

          // POST e atualizar jogador
          final response = await http.post(
            Uri.parse('http://127.0.0.1:8000/rolar-dado/'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'id_jogador': jogador.idJogador, 'valor_dado': result}),
          );

          if (response.statusCode == 200) {
            final jsonResp = jsonDecode(response.body);
            final novaPosicao = jsonResp['nova_posicao'];

            final updatedJogador = jogador.copyWith(
              idCasa: novaPosicao['id_casa'],
              nomeCasa: novaPosicao['nome_casa'],
            );

            ref.refresh(jogadorProvider); // Atualiza tela
            await showDialog(
              context: context,
              builder: (_) => Dialog(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(novaPosicao['nome_casa'] ?? 'Nenhuma ação', textAlign: TextAlign.center, style: const TextStyle(fontSize: 20)),
                      const SizedBox(height: 20),
                      ElevatedButton(onPressed: () => Navigator.of(context).pop(), child: const Text("Ok")),
                    ],
                  ),
                ),
              ),
            );
          }
        },
        child: Image.asset('assets/images/dice.png', fit: BoxFit.cover),
      ),
    );
  }
}
