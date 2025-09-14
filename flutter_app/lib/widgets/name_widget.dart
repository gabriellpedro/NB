// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class PlayerNameWidget extends StatelessWidget {
  final String playerName;

  const PlayerNameWidget({super.key, required this.playerName});

  @override
  Widget build(BuildContext context) {
    return Text(
      'Nome do Jogador: $playerName',
      style: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
      ),
    );
  }
}
