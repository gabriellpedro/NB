import 'package:shared_preferences/shared_preferences.dart';

class LocalStorageService {
  // Identificar os dados no SharedPreferences
  static const String roundIdKey = 'round_id';
  static const String userIdKey = 'user_id';

  // Salvar o round_id e user_id
  Future<void> storeRoundAndUserId(String roundId, String userId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(roundIdKey, roundId);
    await prefs.setString(userIdKey, userId);
  }

  // Recuperar o round_id
  Future<String?> retrieveRoundId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(roundIdKey);
  }

  // Recuperar o user_id
  Future<String?> retrieveUserId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(userIdKey);
  }

  // Remover round_id e user_id
  Future<void> clearStoredRoundAndUserId() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(roundIdKey);
    await prefs.remove(userIdKey);
  }
}
