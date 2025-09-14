// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:nb_game/provider/user_register.dart';
import 'package:nb_game/views/game_page.dart';

class NameRoomForm extends StatefulWidget {
  const NameRoomForm({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _NameRoomFormState createState() => _NameRoomFormState();
}

class _NameRoomFormState extends State<NameRoomForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _roomIdController = TextEditingController();
  final _pinController = TextEditingController();

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
              // Campo de Nome
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
                controller: _pinController,
                decoration: InputDecoration(
                  labelText: 'Cor',
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
              ),
              SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState?.validate() ?? false) {
                    final name = _nameController.text;
                    final roomId = _roomIdController.text.isNotEmpty
                        ? _roomIdController.text
                        : null;
                    final pinColor = _pinController.text;
                    postAndStoreData(context,
                            name: name,
                            birthDate: "2002-04-20",
                            gamePin: pinColor,
                            roundId: roomId)
                        .then((_) {
                      // Navegar para a página de sucesso
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => GamePage()),
                      );
                    }).catchError((error) {
                      // Tratamento de erro
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Falha ao enviar dados: $error'),
                        ),
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
    _pinController.dispose();
    super.dispose();
  }
}
