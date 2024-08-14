// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

Color getColorFromString(String colorString) {
  switch (colorString) {
    case 'azul':
      return Color.fromARGB(1000, 108, 151, 206);
    case 'vermelho':
      return Colors.red;
    case 'verde':
      return Colors.green;
    case 'amarelo':
      return Color.fromARGB(1000, 211, 170, 88);
    case 'roxo':
      return Colors.purple;
    default:
      return Colors.yellow;
  }
}
