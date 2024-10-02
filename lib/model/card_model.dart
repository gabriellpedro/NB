class CardDeck {
  final String? errors;

  CardDeck({
    this.errors,
  });

  factory CardDeck.fromJson(Map<String, dynamic> json) {
    return CardDeck(
      errors: json['errors'] as String?,
    );
  }
}
