// ignore_for_file: prefer_const_constructors, sort_child_properties_last
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/model/user_model_base.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/widgets/build_card.dart';
import 'package:nb_game/widgets/get_color.dart';

class CardConstructor extends ConsumerWidget {
  const CardConstructor({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final apiAsyncValue = ref.watch(userAndDeckProvider);

    return Scaffold(
      appBar: AppBar(),
      body: apiAsyncValue.when(
        data: (gameResponse) {
          List<CardDeck> cardDecks = gameResponse.cardDeck;
          return SizedBox(
            width: 400,
            height: 600,
            child: PageView(
              controller: PageController(viewportFraction: 0.6),
              children: cardDecks.map(
                (cardDeck) {
                  return buildCard(
                    title: Text(
                      'Titulo Carta: ${cardDeck.title}',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    description: Text(
                      'Descrição: ${cardDeck.description}',
                      textAlign: TextAlign.justify,
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                    color: getColorFromString(
                      'azul',
                    ),
                  );
                },
              ).toList(),
            ),
          );
        },
        loading: () => Center(
          child: CircularProgressIndicator(),
        ),
        error: (err, stack) => Center(
          child: Text('Erro: $err'),
        ),
      ),
    );
  }
}
