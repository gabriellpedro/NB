// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class BotaoCoroaWidget extends StatelessWidget {
  const BotaoCoroaWidget({super.key});

  void _abrirSelecaoCartas(BuildContext context) {
    // 🔹 Aqui futuramente abriremos o widget de seleção de cartas
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Abrir seleção de cartas (em breve)")),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Selecionar cartas para deixar em evidência',
      child: SizedBox(
        width: 125,
        height: 125,
        child: ElevatedButton(
          onPressed: () => _abrirSelecaoCartas(context),
          style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            padding: EdgeInsets.all(1),
          ),
          child: Image.asset(
            'assets/images/coroa.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
