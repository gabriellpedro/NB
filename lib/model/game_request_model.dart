class GameRequest {
  final String roundId;
  final String userId;
  final List<dynamic> choices; // pode trocar depois por uma lista de objetos se necessário
  final int diceNumber;
  final bool wantOut;

  GameRequest({
    required this.roundId,
    required this.userId,
    required this.choices,
    required this.diceNumber,
    required this.wantOut,
  });

  Map<String, dynamic> toJson() {
    return {
      'round_id': roundId,
      'user_id': userId,
      'choices': choices,
      'dice_number': diceNumber,
      'want_out': wantOut,
    };
  }
}
