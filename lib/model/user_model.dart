import 'package:intl/intl.dart';

class User {
  final String id;
  final String name;
  final bool? active;
  final String? gamePin;

  User({
    required this.id,
    required this.name,
    this.active,

    this.gamePin,
  });

  User copyWith({
    String? id,
    String? name,
    String? email,
    bool? active,
    String? birthDate,
    DateTime? createdAt,
    String? gamePin,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      active: active ?? this.active,
      gamePin: gamePin ?? this.gamePin,
    );
  }

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      active: json['active'] as bool?,

      gamePin: json['game_pin'] as String?,
    );
  }

}
