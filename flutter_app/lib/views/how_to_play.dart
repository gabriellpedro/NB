// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, sort_child_properties_last

import 'package:flutter/material.dart';
import 'package:nb_game/howtoplay_text.dart';
import 'package:nb_game/widgets/howtoplay_widget.dart';
import 'package:nb_game/widgets/nb_appbar.dart';

class HowToPlay extends StatelessWidget {
  const HowToPlay({super.key});

  @override
  Widget build(BuildContext context) {
    Map<String, String> obterDadosHowToPlay = howToPlayText();
    String howToPlayTextCard = obterDadosHowToPlay.entries
        .map((entry) => '${entry.key}. ${entry.value}\n\n')
        .join();

    Map<String, String> obterDadosComponents = components();
    String componentsTextCard = obterDadosComponents.entries
        .map((entry) => '${entry.key}. ${entry.value}\n')
        .join();

    return Scaffold(
      appBar: GradientAppBar(
        title: 'NB',
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              alignment: Alignment.topCenter,
              padding: EdgeInsets.only(left: 10, right: 10, top: 30),
              child: Column(
                children: [
                  HowToPlayInstructCard(
                    nameCard: 'Como Jogar?',
                    textCard: howToPlayTextCard,
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  HowToPlayInstructCard(
                    nameCard: 'Compontentes',
                    textCard: componentsTextCard,
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  HowToPlayInstructCard(
                    nameCard: 'Objetivo',
                    textCard: objective(),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  HowToPlayInstructCard(
                    nameCard: 'Conclusão',
                    textCard: conclusion(),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
