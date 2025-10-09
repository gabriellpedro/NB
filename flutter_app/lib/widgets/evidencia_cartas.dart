// ignore_for_file: prefer_const_constructors, sort_child_properties_last, use_build_context_synchronously
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:nb_game/provider/user_provider.dart';
import 'package:nb_game/widgets/build_card.dart';
import 'package:nb_game/widgets/get_color.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class BotaoCoroaWidget extends ConsumerStatefulWidget {
  const BotaoCoroaWidget({super.key});

  @override
  ConsumerState<BotaoCoroaWidget> createState() => _BotaoCoroaWidgetState();
}

class _BotaoCoroaWidgetState extends ConsumerState<BotaoCoroaWidget> {
  Map<String, dynamic>? cartasEvidencia;
  List<Map<String, dynamic>> todasCartas = [];

  Future<void> _fetchCartasEvidencia(int idJogador) async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/consulta-carta-evidencia/$idJogador'),
      );

      if (response.statusCode == 200) {
        final decodedBody = utf8.decode(response.bodyBytes);
        final data = json.decode(decodedBody);
        setState(() {
          cartasEvidencia = data['cartas_evidencia'];
        });
      }
    } catch (e) {
      print("Erro ao buscar cartas evidência: $e");
    }
  }

  Future<void> _fetchTodasCartas(int idJogador) async {
    try {
      final response = await http
          .get(Uri.parse('http://127.0.0.1:8000/jogador/$idJogador/cartas'));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        final List cartasList = data['cartas'] ?? [];
        todasCartas = cartasList
            .map<Map<String, dynamic>>((c) => {
                  'id_carta': c['id_carta'],
                  'nome_carta': c['nome_carta'],
                  'descricao_carta': c['descricao_carta'] ?? "",
                  'cor_carta': c['cor_carta'] ?? 'grey',
                  'tipo_carta':
                      (c['tipo_carta'] as String?)?.toLowerCase().trim() ??
                          'inicio',
                })
            .toList();
      }
    } catch (e) {
      print("Erro ao buscar todas as cartas: $e");
    }
  }

  Future<void> _adicionarCarta(
      int idJogador, int controle, int idCarta, BuildContext context) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/alterar-carta-evidencia/'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "id_jogador": idJogador,
        "controle": controle,
        "id_carta": idCarta,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(utf8.decode(response.bodyBytes));
      final mensagem = data['mensagem'] ?? "Carta adicionada com sucesso!";
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(mensagem)));

      await _fetchCartasEvidencia(idJogador);
      setState(() {});
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erro ao adicionar carta.")),
      );
    }
  }

  Future<void> _openCardSelectionDialog(
      BuildContext context, int idJogador, String tipo, int controle) async {
    // Buscar sempre as cartas atualizadas
    await _fetchTodasCartas(idJogador);

    final cartasFiltradas = todasCartas.where((c) {
      final tipoCarta =
          (c['tipo_carta'] as String?)?.toLowerCase().trim() ?? '';
      final tipoFiltro = tipo.toLowerCase();
      return tipoCarta == tipoFiltro ||
          (tipoFiltro == 'fim' && tipoCarta == 'final');
    }).toList();

    if (cartasFiltradas.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Você não possui cartas deste tipo.")),
      );
      return;
    }

    String? selectedCardId;

    if (!context.mounted) return;

    showDialog(
      context: context,
      builder: (_) => StatefulBuilder(builder: (context, setStateDialog) {
        return AlertDialog(
          title: Text("Selecione uma carta ($tipo)"),
          content: SizedBox(
            width: double.maxFinite,
            height: 300,
            child: ListView.builder(
              itemCount: cartasFiltradas.length,
              itemBuilder: (context, index) {
                final carta = cartasFiltradas[index];
                return ListTile(
                  title: Text(carta['nome_carta']),
                  subtitle: Text(
                    carta['descricao_carta'],
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  leading: Radio<String>(
                    value: carta['id_carta'].toString(),
                    groupValue: selectedCardId,
                    onChanged: (value) {
                      setStateDialog(() {
                        selectedCardId = value;
                      });
                    },
                  ),
                  onTap: () {
                    setStateDialog(() {
                      selectedCardId = carta['id_carta'].toString();
                    });
                  },
                );
              },
            ),
          ),
          actions: [
            TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text("Cancelar")),
            ElevatedButton(
              onPressed: selectedCardId != null
                  ? () async {
                      await _adicionarCarta(idJogador, controle,
                          int.parse(selectedCardId!), context);
                      Navigator.of(context).pop();
                    }
                  : null,
              child: const Text("Confirmar"),
            ),
          ],
        );
      }),
    );
  }

  Future<void> _abrirSelecaoCartasPopup(
      BuildContext context, int idJogador) async {
    // 🔁 Sempre atualiza antes de abrir
    await _fetchCartasEvidencia(idJogador);
    await _fetchTodasCartas(idJogador);

    await showDialog(
      context: context,
      barrierDismissible: true,
      builder: (context) {
        return Dialog(
          backgroundColor: Colors.white,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Container(
            width: 1100,
            height: 600,
            padding: EdgeInsets.all(24),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Center(
                    child: Text(
                      'Seleção de Cartas',
                      style:
                          TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(height: 30),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildCardContainer(context, 'Carta Início',
                          cartasEvidencia?['inicio'], idJogador, 1),
                      _buildCardContainer(context, 'Carta Meio',
                          cartasEvidencia?['meio'], idJogador, 2),
                      _buildCardContainer(context, 'Carta Fim',
                          cartasEvidencia?['fim'], idJogador, 3),
                    ],
                  ),
                  SizedBox(height: 20),
                  Align(
                    alignment: Alignment.bottomRight,
                    child: TextButton(
                      onPressed: () => Navigator.pop(context),
                      style: TextButton.styleFrom(
                        backgroundColor: Colors.white,
                        side: BorderSide(color: Colors.deepPurple, width: 2),
                        padding:
                            EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8)),
                      ),
                      child: Text(
                        'Fechar',
                        style: TextStyle(
                            color: Colors.deepPurple,
                            fontSize: 16,
                            fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );

    // 🔁 Atualiza novamente depois de fechar o popup
    await _fetchCartasEvidencia(idJogador);
    setState(() {});
  }

  Widget _buildCardContainer(BuildContext context, String titulo,
      Map<String, dynamic>? cartaData, int idJogador, int controle) {
    String tipo = '';
    switch (controle) {
      case 1:
        tipo = 'inicio';
        break;
      case 2:
        tipo = 'meio';
        break;
      case 3:
        tipo = 'final';
        break;
    }

    Map<String, dynamic>? cartaParaExibir;
    if (cartaData != null &&
        cartaData['id_carta'] != null &&
        cartaData['id_carta'] != 0) {
      cartaParaExibir = todasCartas.firstWhere(
        (c) => c['id_carta'] == cartaData['id_carta'],
        orElse: () => {},
      );
      if (cartaParaExibir.isEmpty) cartaParaExibir = null;
    }

    return Column(
      children: [
        Text(titulo,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(height: 8),
        Container(
          width: 250,
          height: 350,
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: Colors.white,
            border: Border.all(color: Colors.grey[400]!),
            borderRadius: BorderRadius.circular(16),
            boxShadow: const [
              BoxShadow(
                  color: Colors.black12, blurRadius: 4, offset: Offset(2, 2))
            ],
          ),
          child: cartaParaExibir != null
              ? buildCard(
                  title: Text(
                    cartaParaExibir['nome_carta'],
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Colors.white),
                  ),
                  description: Text(
                    cartaParaExibir['descricao_carta'],
                    textAlign: TextAlign.justify,
                    style: const TextStyle(fontSize: 16),
                  ),
                  color: getColorFromString(cartaParaExibir['cor_carta']),
                )
              : const Center(
                  child: Text(
                    'Sem carta adicionada.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.grey, fontSize: 16),
                  ),
                ),
        ),
        const SizedBox(height: 12),
        ElevatedButton(
          onPressed: () =>
              _openCardSelectionDialog(context, idJogador, tipo, controle),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.deepPurple,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 10),
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          ),
          child: const Text('Adicionar carta',
              style: TextStyle(color: Colors.white)),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final jogadorAsync = ref.watch(jogadorProvider);

    return jogadorAsync.when(
      data: (jogador) {
        return Tooltip(
          message: 'Selecionar cartas para deixar em evidência',
          child: SizedBox(
            width: 125,
            height: 125,
            child: ElevatedButton(
              onPressed: () =>
                  _abrirSelecaoCartasPopup(context, jogador.idJogador),
              style: ElevatedButton.styleFrom(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8)),
                padding: EdgeInsets.all(1),
              ),
              child: Image.asset('assets/images/coroa.png', fit: BoxFit.cover),
            ),
          ),
        );
      },
      loading: () => const CircularProgressIndicator(),
      error: (err, _) =>
          Text('Erro: $err', style: const TextStyle(color: Colors.red)),
    );
  }
}
