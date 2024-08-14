// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class buildCard extends StatelessWidget {
  final Text title;
  final Text description;
  final Color color;

  const buildCard(
      {super.key,
      required this.title,
      required this.description,
      required this.color});

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity,
            color: color,
            padding: EdgeInsets.all(16.0),
            child: title,
          ),
          Expanded(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: description,
            ),
          ),
        ],
      ),
    );
  }
}
