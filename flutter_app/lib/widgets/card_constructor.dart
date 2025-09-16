// ignore_for_file: prefer_const_constructors, sort_child_properties_last
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/model/game_request_model.dart'; // Jogador e Carta
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/widgets/build_card.dart';
import 'package:nb_game/widgets/get_color.dart';

class CardConstructor extends ConsumerStatefulWidget {
  const CardConstructor({super.key});

  @override
  _CardConstructorState createState() => _CardConstructorState();
}

class _CardConstructorState extends ConsumerState<CardConstructor> {
  late PageController _pageController;

  @override
  void initState() {
    super.initState();
    _pageController = PageController(viewportFraction: 0.15);
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final jogadorAsync = ref.watch(jogadorProvider);

    return jogadorAsync.when(
      data: (jogador) {
        List<Carta> cartas = jogador.cartas;

        if (cartas.isEmpty) {
          return Center(
            child: Text(
              "Nenhuma carta encontrada",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          );
        }

        return PageView.builder(
          controller: _pageController,
          itemCount: cartas.length,
          itemBuilder: (context, index) {
            return AnimatedBuilder(
              animation: _pageController,
              builder: (context, child) {
                double scale = 1.0;
                if (_pageController.position.haveDimensions) {
                  double page = _pageController.page ??
                      _pageController.initialPage.toDouble();
                  scale = 0.9 + (1 - (page - index).abs()) * 0.1;
                  scale = scale.clamp(0.9, 1.0);
                }
                return Transform.scale(
                  scale: scale,
                  child: child,
                );
              },
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: buildCard(
                  title: Text(
                    cartas[index].nomeCarta,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  description: Text(
                    cartas[index].descricaoCarta,
                    textAlign: TextAlign.justify,
                    style: TextStyle(fontSize: 16),
                  ),
                  color: getColorFromString(cartas[index].corCarta),
                ),
              ),
            );
          },
        );
      },
      loading: () => Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Erro: $err')),
    );
  }
}
