// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:nb_game/widgets/chat_widget.dart';
import 'package:nb_game/widgets/give_a_turn.dart';
import 'package:nb_game/widgets/see_card.dart';

class ButtonConstuctor extends StatelessWidget {
  const ButtonConstuctor({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SizedBox(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 64.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Tooltip(
                  message: 'Rolar o Dado',
                  child: SizedBox(
                    width: 125, // Define largura para manter alinhamento
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
                        'assets/images/dice.png',
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 60),
                Tooltip(
                  message: 'Descartar Carta',
                  child: SizedBox(
                    width: 125, // Define largura para manter alinhamento
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
                ),
                SizedBox(width: 60),
                Tooltip(
                  message: 'Pegar Nova Carta',
                  child: SizedBox(
                    width: 125, // Define largura para manter alinhamento
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
                        'assets/images/pegar_carta.png',
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 60),
                ChatButton(),
                SizedBox(width: 60),
                SelecaoJogadorButton(),
                SizedBox(width: 60),
                PlayerSelectionButton()
              ],
            ),
          ),
        ),
      ),
    );
  }
}
