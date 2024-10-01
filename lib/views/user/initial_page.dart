// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:nb_game/views/game_page.dart';
import 'package:nb_game/views/providers/how_to_play.dart';

class InitialPage extends StatelessWidget {
  const InitialPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: EdgeInsets.only(top: 175, left: 40, right: 40),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color.fromARGB(1000, 108, 151, 206),
              Color.fromARGB(1000, 132, 84, 170),
              Color.fromARGB(1000, 211, 170, 88),
              Color.fromARGB(1000, 213, 100, 80),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: ListView(
          children: <Widget>[
            SizedBox(
              width: 275,
              height: 275,
              child: Image.asset('assets/images/initialpagelogo.png'),
            ),
            SizedBox(
              height: 50,
            ),
            SizedBox(
              width: 10,
              height: 65,
              child: FilledButton(
                style: FilledButton.styleFrom(
                  backgroundColor: Color.fromARGB(
                    1000,
                    108,
                    151,
                    206,
                  ),
                  side: BorderSide(
                    color: Colors.black,
                    width: 2,
                  ),
                ),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => HowToPlay()),
                  );
                },
                child: Text(
                  'Como Jogar?',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                    fontSize: 28,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            SizedBox(
              height: 20,
            ),
            SizedBox(
              width: 10,
              height: 65,
              child: FilledButton(
                style: FilledButton.styleFrom(
                  backgroundColor: Color.fromARGB(
                    1000,
                    211,
                    170,
                    88,
                  ),
                  side: BorderSide(
                    color: Colors.black,
                    width: 2,
                  ),
                ),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => GamePage()),
                  );
                },
                child: Text(
                  'Iniciar',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                    fontSize: 28,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            SizedBox(
              height: 60,
            ),
            Text(
              'E.M.T.I. Profª Maria Joaquina de Arruda\nLeme-SP',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 17,
              ),
            )
          ],
        ),
      ),
    );
  }
}
