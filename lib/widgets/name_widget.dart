// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class PlayerNameWidget extends StatelessWidget {
  final Future<String> fetchPlayerName;

  const PlayerNameWidget({required this.fetchPlayerName});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String>(
      future: fetchPlayerName,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return CircularProgressIndicator();
        } else if (snapshot.hasError) {
          return Text('Erro: ${snapshot.error}');
        } else if (snapshot.hasData) {
          return Text(
            'Nome do Jogador: ${snapshot.data}',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          );
        } else {
          return Text('Nenhum dado disponível');
        }
      },
    );
  }
}
