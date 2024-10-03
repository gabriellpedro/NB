// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/widgets/board_position_widget.dart';
import 'package:nb_game/widgets/card_constructor.dart';
import 'package:nb_game/widgets/dice_widget.dart';
import 'package:nb_game/widgets/name_widget.dart';

class GamePage extends ConsumerWidget {
  const GamePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsyncValue = ref.watch(userAndDeckProvider);

    return Scaffold(
      body: Column(
        children: [
          SizedBox(
            height: 100,
          ),
          userAsyncValue.when(
            data: (user) {
              return PlayerNameWidget(
                playerName: user.user.name.toString(),
              );
            },
            loading: () => CircularProgressIndicator(),
            error: (err, stack) => Text('Erro: $err'),
          ),
          Expanded(
            child: CardConstructor(),
          ),
          SizedBox(
            height: 50,
          ),
          PositionWidget(
            position: '1º Casa',
          ),
          Expanded(
            child: ButtonConstuctor(),
          ),
        ],
      ),
    );
  }
}
