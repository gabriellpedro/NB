// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:nb_game/widgets/chat_widget.dart';
import 'package:nb_game/widgets/give_a_turn.dart';
import 'package:nb_game/widgets/see_card.dart';

class ButtonDiscard extends StatelessWidget {
  const ButtonDiscard({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Descartar Carta',
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
          onPressed: () {},
          child: Image.asset(
            'assets/images/descarte_carta.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
