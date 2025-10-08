// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, unused_result
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/provider/notification_provider.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/services/notification_service.dart';
import 'package:nb_game/widgets/board_position_widget.dart';
import 'package:nb_game/widgets/card_constructor.dart';
import 'package:nb_game/widgets/button_constructor.dart';
import 'package:nb_game/widgets/evidencia_cartas.dart';
import 'package:nb_game/widgets/name_widget.dart';
import 'package:nb_game/widgets/round_id_label.dart';

class GamePage extends ConsumerStatefulWidget {
  const GamePage({super.key});

  @override
  ConsumerState<GamePage> createState() => _GamePageState();
}

class _GamePageState extends ConsumerState<GamePage> {
  bool _popupAberto = false; // 🔒 Controle de popup

  @override
  void initState() {
    super.initState();

    // Polling a cada 5 segundos
    Future.doWhile(() async {
      await Future.delayed(const Duration(seconds: 5));

      if (_popupAberto) {
        return true;
      }

      final jogador = await ref.read(jogadorProvider.future);
      final notificacoes =
          await ref.read(notificacoesProvider(jogador.idJogador).future);

      if (notificacoes.isNotEmpty && mounted) {
        final notificacao = notificacoes.first;

        _popupAberto = true;
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (_) => AlertDialog(
            title: const Text("Notificação"),
            content: Text(notificacao["mensagem"]),
            actions: [
              TextButton(
                child: const Text("Ok"),
                onPressed: () async {
                  Navigator.of(context).pop();
                  await marcarNotificacaoProcessada(notificacao["id"]);
                  ref.refresh(jogadorProvider);
                  ref.refresh(notificacoesProvider(jogador.idJogador));
                  _popupAberto = false;
                },
              ),
            ],
          ),
        );
      }

      return true;
    });
  }

  @override
  Widget build(BuildContext context) {
    final jogadorAsync = ref.watch(jogadorProvider);

    return Scaffold(
      body: SafeArea(
        child: jogadorAsync.when(
          data: (jogador) {
            return SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 20),
                  PlayerNameWidget(playerName: jogador.nomeJogador),
                  const SizedBox(height: 20),
                  const CardConstructor(),
                  const SizedBox(height: 50),
                  PositionWidget(
                    position: (jogador.idCasa != null && jogador.nomeCasa != null)
                        ? '${jogador.idCasa} - ${jogador.nomeCasa}'
                        : 'Sem posição',
                  ),
                  const SizedBox(height: 10),
                  const SizedBox(
                    height: 120,
                    child: ButtonConstuctor(),
                  ),
                  const SizedBox(height: 50),

                  // 👇 RoundIdLabelWidget + Botão Coroa lado a lado
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      RoundIdLabelWidget(),
                      const SizedBox(width: 15),
                      SizedBox(
                        width: 70,
                        height: 70,
                        child: BotaoCoroaWidget(),
                      ),
                    ],
                  ),
                ],
              ),
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => Center(
            child: Text(
              'Erro: $err',
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ),
      ),
    );
  }
}
