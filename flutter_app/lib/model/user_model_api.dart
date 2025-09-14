import 'package:nb_game/model/user_model_base.dart';

class GameResponse {
  final List<CardDeck> cardDeck;
  final User user;

  GameResponse({
    required this.cardDeck,
    required this.user,
  });

  factory GameResponse.fromJson(Map<String, dynamic> json) {
    var cardDeckList = json['card_deck'] as List;
    List<CardDeck> cardDeckItems =
        cardDeckList.map((i) => CardDeck.fromJson(i)).toList();

    return GameResponse(
      cardDeck: cardDeckItems,
      user: User.fromJson(json['user']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'card_deck': cardDeck.map((card) => card.toJson()).toList(),
      'user': user.toJson(),
    };
  }
}
