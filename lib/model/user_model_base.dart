class CardDeck {
  final bool activate;
  final String cardId;
  final String createdAt;
  final String description;
  final String id;
  final String place;
  final String roundId;
  final String title;
  final String type;
  final String userId;

  CardDeck({
    required this.activate,
    required this.cardId,
    required this.createdAt,
    required this.description,
    required this.id,
    required this.place,
    required this.roundId,
    required this.title,
    required this.type,
    required this.userId,
  });

  factory CardDeck.fromJson(Map<String, dynamic> json) {
    return CardDeck(
      activate: json['activate'],
      cardId: json['card_id'],
      createdAt: json['created_at'],
      description: json['description'],
      id: json['id'],
      place: json['place'],
      roundId: json['round_id'],
      title: json['title'],
      type: json['type'],
      userId: json['user_id'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'activate': activate,
      'card_id': cardId,
      'created_at': createdAt,
      'description': description,
      'id': id,
      'place': place,
      'round_id': roundId,
      'title': title,
      'type': type,
      'user_id': userId,
    };
  }
}

class User {
  final bool active;
  final String birthDate;
  final String createdAt;
  final String gamePin;
  final String id;
  final String name;

  User({
    required this.active,
    required this.birthDate,
    required this.createdAt,
    required this.gamePin,
    required this.id,
    required this.name,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      active: json['active'],
      birthDate: json['birth_date'],
      createdAt: json['created_at'],
      gamePin: json['game_pin'],
      id: json['id'],
      name: json['name'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'active': active,
      'birth_date': birthDate,
      'created_at': createdAt,
      'game_pin': gamePin,
      'id': id,
      'name': name,
    };
  }
}
