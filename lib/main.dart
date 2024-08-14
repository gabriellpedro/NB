import 'package:flutter/material.dart';
import 'package:nb_game/views/providers/how_to_play.dart';
import 'package:nb_game/views/user/initial_page.dart';
import 'package:nb_game/widgets/card_constructor.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NB',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const CardConstructor(),
    );
  }
}
