// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
// import 'package:nb_game/howtoplay_text.dart';

class HowToPlayInstructCard extends StatelessWidget {
  final String nameCard;
  final String textCard;

  const HowToPlayInstructCard({
    super.key,
    required this.nameCard,
    required this.textCard,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          width: 300,
          height: 65,
          child: FilledButton(
            style: FilledButton.styleFrom(
              backgroundColor: Colors.white,
              side: BorderSide(
                color: Colors.red,
                width: 2,
              ),
            ),
            onPressed: () {},
            child: Text(
              nameCard,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.black,
                fontSize: 28,
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
        Container(
          padding: EdgeInsets.only(right: 20, left: 20, top: 10),
          alignment: Alignment.centerLeft,
          child: Text(
            textCard,
            style: TextStyle(fontSize: 20),
            textAlign: TextAlign.justify,
          ),
        )
      ],
    );
  }
}
