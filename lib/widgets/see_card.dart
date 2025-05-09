// ignore_for_file: prefer_const_constructors, avoid_print, sort_child_properties_last

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/widgets/card_constructor.dart'; // onde está o carrossel

class PlayerSelectionButton extends ConsumerStatefulWidget {
  const PlayerSelectionButton({super.key});

  @override
  ConsumerState<PlayerSelectionButton> createState() =>
      _PlayerSelectionButtonState();
}

class Player {
  final String id;
  final String name;

  Player({required this.id, required this.name});
}

class _PlayerSelectionButtonState extends ConsumerState<PlayerSelectionButton> {
  String? selectedPlayerId;

  Future<void> _sendSelectionToAPI(String playerId) async {
    // Simulação do envio
    await Future.delayed(Duration(milliseconds: 500));
    print('Enviado para API: $playerId');
  }

  void _openPlayerSelectionDialog(BuildContext context) async {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // 🔧 TESTE: Lista fixa de jogadores
        final playerList = AsyncValue.data([
          Player(id: '1', name: 'Jogador 1'),
          Player(id: '2', name: 'Jogador 2'),
          Player(id: '3', name: 'Jogador 3'),
        ]);

        // ✅ LINHA PARA USO REAL VIA API (descomente quando estiver com a API pronta)
        // final playerList = ref.watch(playersProvider);

        return AlertDialog(
          title: Text('Selecione um jogador'),
          content: playerList.when(
            data: (players) {
              return Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  DropdownButton<String>(
                    isExpanded: true,
                    hint: Text('Escolha um jogador'),
                    value: selectedPlayerId,
                    items: players.map<DropdownMenuItem<String>>((player) {
                      return DropdownMenuItem<String>(
                        value: player.id,
                        child: Text(player.name),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedPlayerId = value!;
                      });
                    },
                  ),
                ],
              );
            },
            loading: () => CircularProgressIndicator(),
            error: (e, _) => Text('Erro ao carregar jogadores'),
          ),
          actions: [
            TextButton(
              child: Text('Cancelar'),
              onPressed: () => Navigator.of(context).pop(),
            ),
            ElevatedButton(
              child: Text('Confirmar'),
              onPressed: selectedPlayerId != null
                  ? () async {
                      await _sendSelectionToAPI(selectedPlayerId!);
                      Navigator.of(context).pop(); // Fecha este dialog
                      _showCardCarousel(context); // Abre o carrossel
                    }
                  : null,
            ),
          ],
        );
      },
    );
  }

  void _showCardCarousel(BuildContext context) {
    showDialog(
      context: context,
      builder: (_) => Dialog(
        child: SizedBox(
          width: 400,
          height: 600,
          child: CardConstructor(), // Usa sua lógica com PageView
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Escolher jogador para visualizar o baralho',
      child: SizedBox(
        width: 125,
        height: 125,
        child: ElevatedButton(
          onPressed: () => _openPlayerSelectionDialog(context),
          style: ElevatedButton.styleFrom(
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            padding: const EdgeInsets.all(1),
          ),
          child: Image.asset(
            'assets/images/ver_baralho.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
