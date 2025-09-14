class ResponseModel {
  final String roundId;
  final String userId;

  ResponseModel({
    required this.roundId,
    required this.userId,
  });

  factory ResponseModel.fromJson(Map<String, dynamic> json) {
    return ResponseModel(
      roundId: json['round_id'],
      userId: json['user_id'],
    );
  }
}
