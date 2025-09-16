import 'dart:math';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class DiceButton extends StatefulWidget {
  final String userId;

  const DiceButton({super.key, required this.userId});

  @override
  _DiceButtonState createState() => _DiceButtonState();
}

class _DiceButtonState extends State<DiceButton> {
  int? diceValue;

  Future<void> _rollDice() async {
    final random = Random();
    final result = random.nextInt(6) + 1;

    setState(() {
      diceValue = result;
    });

    // Fazer POST na API
    final apiResponse = await _sendDiceValue(widget.userId, result);

    // Primeiro popup: número do dado
    await _showDiceDialog(result);

    // Segundo popup: ação do jogador (nome_casa)
    if (apiResponse != null) {
      final novaCasa =
          apiResponse['nova_posicao']?['nome_casa'] ?? 'Nenhuma ação';
      await _showActionDialog(novaCasa);
    }
  }

  Future<Map<String, dynamic>?> _sendDiceValue(
      String userId, int diceValue) async {
    final url = Uri.parse(
        'http://127.0.0.1:8000/rolar-dado/'); // ⚠️ ajuste conforme sua URL
    final body = jsonEncode({
      "id_jogador": userId,
      "valor_dado": diceValue,
    });

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print('Erro ao enviar dado: ${response.statusCode} - ${response.body}');
        return null;
      }
    } catch (e) {
      print('Erro na requisição: $e');
      return null;
    }
  }

  Future<void> _showDiceDialog(int result) {
    return showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  "Você tirou: $result",
                  style: const TextStyle(
                      fontSize: 22, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text("Ok"),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Future<void> _showActionDialog(String action) {
    return showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  action,
                  style: const TextStyle(fontSize: 20),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text("Ok"),
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
