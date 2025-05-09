import 'package:flutter/material.dart';

class ChatButton extends StatefulWidget {
  const ChatButton({super.key});

  @override
  State<ChatButton> createState() => _ChatButtonState();
}

class _ChatButtonState extends State<ChatButton> {
  final List<String> _messages = [];
  final TextEditingController _controller = TextEditingController();

  String? _selectedUser;
  final List<String> _users = ['Alice', 'Bob', 'Carlos']; // Simulados para exemplo

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isNotEmpty && _selectedUser != null) {
      setState(() {
        _messages.add('Para $_selectedUser: $text');
      });
      _controller.clear();

      // Aqui você chamaria sua API usando _selectedUser e text
    }
  }

  void _showChatPopup(BuildContext context) {
    showDialog(
      context: context,
      builder: (_) {
        return Dialog(
          insetPadding: const EdgeInsets.all(40),
          child: Container(
            width: 300,
            height: 460,
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        title: Text(_messages[index]),
                      );
                    },
                  ),
                ),
                const Divider(),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _controller,
                        decoration: const InputDecoration(
                          hintText: 'Digite sua mensagem',
                        ),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.send),
                      onPressed: _sendMessage,
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                DropdownButtonFormField<String>(
                  value: _selectedUser,
                  hint: const Text('Selecione o destinatário'),
                  onChanged: (String? value) {
                    setState(() {
                      _selectedUser = value;
                    });
                  },
                  items: _users.map((String user) {
                    return DropdownMenuItem<String>(
                      value: user,
                      child: Text(user),
                    );
                  }).toList(),
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    contentPadding: EdgeInsets.symmetric(horizontal: 12),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Enviar elogio',
      child: SizedBox(
        width: 125,
        height: 125,
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.all(1),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          onPressed: () => _showChatPopup(context),
          child: Image.asset(
            'assets/images/elogio.png',
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
