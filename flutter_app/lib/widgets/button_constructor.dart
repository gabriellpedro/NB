import 'package:flutter/material.dart';
import 'package:nb_game/storage/storage_preferences.dart';
import 'package:nb_game/widgets/dice_button.dart';
import 'package:nb_game/widgets/discard_cart.dart';
import 'package:nb_game/widgets/pickup_card.dart';
import 'package:nb_game/widgets/chat_widget.dart';
import 'package:nb_game/widgets/give_a_turn.dart';
import 'package:nb_game/widgets/see_card.dart';

class ButtonConstuctor extends StatelessWidget {
  const ButtonConstuctor({super.key});

  @override
  Widget build(BuildContext context) {
    final storage = LocalStorageService();

    return FutureBuilder(
      future: Future.wait([
        storage.retrieveRoundId(),
        storage.retrieveUserId(),
      ]),
      builder: (context, AsyncSnapshot<List<dynamic>> snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }

        if (snapshot.hasError || snapshot.data == null) {
          return const Center(child: Text("Erro ao carregar dados do jogador"));
        }

        final roundId = snapshot.data![0] as String;
        final userId = snapshot.data![1] as String;

        return Scaffold(
          body: Center(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  DiceButton(userId: userId),
                  const SizedBox(width: 60),
                  const ButtonDiscard(),
                  const SizedBox(width: 60),
                  const ButtonPickup(),
                  const SizedBox(width: 60),
                  const ChatButton(),
                  const SizedBox(width: 60),
                  const SelecaoJogadorButton(),
                  const SizedBox(width: 60),
                  const PlayerSelectionButton(),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
