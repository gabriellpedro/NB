// ignore_for_file: prefer_const_constructors, sort_child_properties_last
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
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
          return const Center(
            child: Text(
              'Nenhuma carta encontrada',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          );
        }

        final pageController = PageController(viewportFraction: 0.15);

        return SizedBox(
          height: 300,
          child: ScrollConfiguration(
            behavior: const ScrollBehavior()
                .copyWith(scrollbars: false), // Remove scrollbars nativos pequenos
            child: RawScrollbar(
              thumbColor: Colors.blueGrey,
              radius: const Radius.circular(8),
              thickness: 12, // Tamanho maior da barra
              crossAxisMargin: 2,
              mainAxisMargin: 2,
              controller: pageController,
              child: Listener(
                onPointerSignal: (pointerSignal) {
                  if (pointerSignal is PointerScrollEvent) {
                    // Permite rolar pelo scroll do mouse
                    pageController.position.moveTo(
                      pageController.position.pixels + pointerSignal.scrollDelta.dy,
                    );
                  }
                },
                child: PageView.builder(
                  itemCount: cartas.length,
                  controller: pageController,
                  scrollDirection: Axis.horizontal,
                  itemBuilder: (context, index) => Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8),
                    child: buildCard(
                      title: Text(
                        cartas[index].nomeCarta,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      description: Text(
                        cartas[index].descricaoCarta,
                        textAlign: TextAlign.justify,
                        style: const TextStyle(fontSize: 16),
                      ),
                      color: getColorFromString(
                        cartas[index].corCarta,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      },
      loading: () => const Center(
        child: CircularProgressIndicator(),
      ),
      error: (err, _) => Center(
        child: Text(
          'Erro: $err',
          style: const TextStyle(color: Colors.red),
        ),
      ),
    );
  }
}
