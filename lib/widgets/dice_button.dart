import 'dart:math';
import 'package:flutter/material.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/storage/storage_preferences.dart';

class DiceButton extends StatefulWidget {
  final String roundId;
  final String userId;

  const DiceButton({super.key, required this.roundId, required this.userId});

  @override
  _DiceButtonState createState() => _DiceButtonState();
}

class _DiceButtonState extends State<DiceButton> {
  int? diceValue;

  void _rollDice() async {
    final random = Random();
    final result = random.nextInt(6) + 1;

    setState(() {
      diceValue = result;
    });

    // Salvar no SharedPreferences
    final localStorageService = LocalStorageService();
    await localStorageService.storeRoundAndUserId(widget.roundId, widget.userId);
    await localStorageService.storeDiceValue(result);

    // Abrir o popup
    _showDiceDialog(result);
  }

  void _showDiceDialog(int result) {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  "Você tirou: $result",
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () async {
                    final localStorageService = LocalStorageService();

                    final roundId = await localStorageService.retrieveRoundId();
                    final userId = await localStorageService.retrieveUserId();
                    final diceValue = await localStorageService.retrieveDiceValue();

                    if (roundId != null && userId != null && diceValue != null) {
                      await sendGameData(
                        roundId: roundId,
                        userId: userId,
                        diceNumber: diceValue,
                        choices: [],
                        wantOut: false,
                      );
                    } else {
                      print('Dados insuficientes para enviar.');
                    }

                    Navigator.of(context).pop(); // Fecha o popup
                  },
                  child: const Text("Fechar"),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 125,
      height: 125,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.all(1),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        ),
        onPressed: _rollDice,
        child: Image.asset(
          'assets/images/dice.png',
          fit: BoxFit.cover,
        ),
      ),
    );
  }
}
