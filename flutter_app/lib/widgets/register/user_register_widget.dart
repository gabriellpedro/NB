// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:nb_game/provider/user_register.dart';
import 'package:nb_game/views/game_page.dart';

class NameRoomForm extends StatefulWidget {
  const NameRoomForm({super.key});

  @override
  _NameRoomFormState createState() => _NameRoomFormState();
}

class _NameRoomFormState extends State<NameRoomForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _roomIdController = TextEditingController();
  final _colorController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Nome e Sala'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Nome',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira o nome';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),
              TextFormField(
                controller: _colorController,
                decoration: InputDecoration(
                  labelText: 'Cor do Peão',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira a cor de seu peão';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),
              TextFormField(
                controller: _roomIdController,
                decoration: InputDecoration(
                  labelText: 'ID da Sala (opcional)',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
              ),
              SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState?.validate() ?? false) {
                    final nomeJogador = _nameController.text;
                    final corJogador = _colorController.text;
                    final idPartida = _roomIdController.text.isNotEmpty
                        ? int.tryParse(_roomIdController.text)
                        : null; // null se vazio

                    postAndStoreData(
                      context,
                      nomeJogador: nomeJogador,
                      corJogador: corJogador,
                      idPartida: idPartida, // envia null se não informado
                    ).then((_) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => GamePage()),
                      );
                    }).catchError((error) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Falha ao enviar dados: $error')),
                      );
                    });
                  }
                },
                child: Text('Enviar'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _roomIdController.dispose();
    _colorController.dispose();
    super.dispose();
  }
}
