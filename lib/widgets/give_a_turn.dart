import 'package:flutter/material.dart';

// Simulação de chamada de API para buscar jogadores
Future<List<String>> fetchJogadores() async {
  await Future.delayed(Duration(seconds: 1)); // simula delay
  return ['Alice', 'Bob', 'Carlos', 'Diana'];
}

// Simulação da função que será chamada após selecionar
void executarAcaoCom(String jogadorSelecionado) {
  print("Ação enviada para $jogadorSelecionado");
}

class SelecaoJogadorButton extends StatefulWidget {
  const SelecaoJogadorButton({super.key});

  @override
  State<SelecaoJogadorButton> createState() => _SelecaoJogadorButtonState();
}

class _SelecaoJogadorButtonState extends State<SelecaoJogadorButton> {
  String? jogadorSelecionado;

  void _abrirSelecaoJogador() async {
    final jogadores = await fetchJogadores();

    showDialog(
      context: context,
      builder: (context) {
        String? jogadorTemp = jogadorSelecionado;

        return AlertDialog(
          title: Text('Escolha o jogador'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              DropdownButtonFormField<String>(
                value: jogadorTemp,
                items: jogadores
                    .map((jogador) => DropdownMenuItem(
                          value: jogador,
                          child: Text(jogador),
                        ))
                    .toList(),
                onChanged: (value) {
                  jogadorTemp = value;
                },
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Cancelar'),
            ),
            ElevatedButton(
              onPressed: () {
                if (jogadorTemp != null) {
                  setState(() {
                    jogadorSelecionado = jogadorTemp!;
                  });
                  executarAcaoCom(jogadorTemp!);
                  Navigator.pop(context);
                }
              },
              child: Text('Confirmar'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Escolher jogador ceder a vez',
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
          onPressed: _abrirSelecaoJogador,
          child: Image.asset(
            'assets/images/turno.png',
            fit: BoxFit.cover,
          ), // Ou imagem personalizada
        ),
      ),
    );
  }
}
