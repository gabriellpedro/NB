// ignore_for_file: prefer_const_constructors, sort_child_properties_last

import 'package:flutter/material.dart';
import 'package:nb_game/views/providers/card_info_function.dart';
import 'package:nb_game/widgets/build_card.dart';
import 'package:nb_game/widgets/get_color.dart';

class CardConstructor extends StatelessWidget {
  const CardConstructor({super.key});

  @override
  Widget build(BuildContext context) {
    Map<int, Map<String, String>> dados = infoCard();

    List<int> listaDeCardsPlayer = [1, 4, 7];

    return Scaffold(
      appBar: AppBar(
        title: Text('Map com IDs, Títulos e Descrições'),
      ),
      body: SizedBox(
        width: 400,
        height: 500,
        child: PageView(
          controller: PageController(viewportFraction: 0.6),
          children:
              listaDeCardsPlayer.where((key) => dados.containsKey(key)).map(
            (key) {
              return buildCard(
                title: Text(
                  dados[key]!['Titulo'] ?? 'Sem Título',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                description: Text(
                  dados[key]!['Descricao'] ?? 'Sem Descrição',
                  textAlign: TextAlign.justify,
                  style: TextStyle(
                    fontSize: 20,
                  ),
                ),
                color: getColorFromString(
                  dados[key]!['Color'] ?? 'azul',
                ),
              );
            },
          ).toList(),
        ),
      ),
    );
  }
}






// Card(
//               child: ListTile(
//                 title: Text(dados[key]!['Titulo'] ?? 'Sem Título'),
//                 subtitle: Text(dados[key]!['Descricao'] ?? 'Sem Descrição'),
//               ),
//             );