// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/widgets/board_position_widget.dart';
import 'package:nb_game/widgets/card_constructor.dart';
import 'package:nb_game/widgets/button_constructor.dart';
import 'package:nb_game/widgets/name_widget.dart';
import 'package:nb_game/widgets/round_id_label.dart';

class GamePage extends ConsumerWidget {
  const GamePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final jogadorAsync = ref.watch(jogadorProvider);

    return Scaffold(
      body: SafeArea(
        child: jogadorAsync.when(
          data: (jogador) {
            return SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 20),
                  PlayerNameWidget(
                    playerName: jogador.nomeJogador,
                  ),
                  const SizedBox(height: 20),

                  // Cartas do jogador
                  SizedBox(
                    height: 300,
                    child: CardConstructor(),
                  ),

                  const SizedBox(height: 50),
                  PositionWidget(
                    position:
                        (jogador.idCasa != null && jogador.nomeCasa != null)
                            ? '${jogador.idCasa} - ${jogador.nomeCasa}'
                            : 'Sem posição',
                  ),

                  const SizedBox(height: 10),

                  SizedBox(
                    height: 120,
                    child: ButtonConstuctor(),
                  ),

                  const SizedBox(height: 50),
                  RoundIdLabelWidget(),
                ],
              ),
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, stack) => SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                'Erro: $err',
                style: const TextStyle(color: Colors.red),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
