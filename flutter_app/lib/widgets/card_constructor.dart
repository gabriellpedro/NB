// ignore_for_file: prefer_const_constructors, sort_child_properties_last
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/model/game_request_model.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/widgets/build_card.dart';
import 'package:nb_game/widgets/get_color.dart';

class CardConstructor extends ConsumerWidget {
  const CardConstructor({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final jogadorAsync = ref.watch(jogadorProvider);

    return jogadorAsync.when(
      data: (jogador) {
        final cartas = jogador.cartas;
        if (cartas.isEmpty) {
          return const Center(child: Text("Nenhuma carta encontrada", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)));
        }

        return SizedBox(
          height: 300,
          child: PageView.builder(
            itemCount: cartas.length,
            controller: PageController(viewportFraction: 0.15),
            itemBuilder: (context, index) => Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: buildCard(
                title: Text(cartas[index].nomeCarta, textAlign: TextAlign.center, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white)),
                description: Text(cartas[index].descricaoCarta, textAlign: TextAlign.justify, style: const TextStyle(fontSize: 16)),
                color: getColorFromString(cartas[index].corCarta),
              ),
            ),
          ),
        );
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, _) => Center(child: Text('Erro: $err', style: const TextStyle(color: Colors.red))),
    );
  }
}
