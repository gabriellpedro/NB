// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:nb_game/widgets/board_position_widget.dart';
import 'package:nb_game/widgets/card_constructor.dart';
import 'package:nb_game/widgets/dice_widget.dart';
import 'package:nb_game/widgets/name_widget.dart';

class GamePage extends StatelessWidget {
  const GamePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          SizedBox(
            height: 100,
          ),
          PlayerNameWidget(
            fetchPlayerName: Future(() => 'Leandro'),
          ),
          Expanded(
            child: CardConstructor(),
          ),
          SizedBox(
            height: 50,
          ),
          PositionWidget(
            position: '1 - Casa do LEANDRO',
          ),
          Expanded(
            child: ButtonConstuctor(),
          ),
        ],
      ),
    );
  }
}
