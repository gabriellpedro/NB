// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter/services.dart'; // Para usar o Clipboard
import 'package:shared_preferences/shared_preferences.dart';

class LocalStorageService {
  static const String roundIdKey = 'round_id';

  // Recuperar o round_id
  Future<String?> retrieveRoundId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(roundIdKey);
  }
}

class RoundIdLabelWidget extends StatelessWidget {
  final localStorageService = LocalStorageService();

  RoundIdLabelWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String?>(
      future: localStorageService.retrieveRoundId(),
      builder: (BuildContext context, AsyncSnapshot<String?> snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Text('Erro ao carregar código da sala');
        } else if (!snapshot.hasData || snapshot.data == null) {
          return Text('Nenhum código de sala disponível');
        } else {
          final roundId = snapshot.data!;

          return Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                'Código sala: ',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Exibir o roundId em um container
                  Container(
                    padding: EdgeInsets.all(4),
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: Colors.black,
                        width: 1,
                      ),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      roundId,
                      style: TextStyle(
                        fontSize: 18,
                      ),
                    ),
                  ),
                  SizedBox(width: 8),
                  // Botão de copiar
                  IconButton(
                    icon: Icon(Icons.copy),
                    onPressed: () {
                      Clipboard.setData(ClipboardData(text: roundId));
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Código copiado!'),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ],
          );
        }
      },
    );
  }
}
