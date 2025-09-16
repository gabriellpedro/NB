// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'package:flutter/material.dart';
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
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: const [
          DiceButton(),
          SizedBox(width: 60),
          ButtonDiscard(),
          SizedBox(width: 60),
          ButtonPickup(),
          SizedBox(width: 60),
          ChatButton(),
          SizedBox(width: 60),
          SelecaoJogadorButton(),
          SizedBox(width: 60),
          PlayerSelectionButton(),
        ],
      ),
    );
  }
}
