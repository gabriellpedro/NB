import 'package:shared_preferences/shared_preferences.dart';

class LocalStorageService {
  // Identificar os dados no SharedPreferences
  static const String roundIdKey = 'round_id';
  static const String userIdKey = 'user_id';
  static const String diceValueKey = 'dice_value';

  // Salvar round_id e user_id
  Future<void> storeRoundAndUserId(String roundId, String userId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(roundIdKey, roundId);
    await prefs.setString(userIdKey, userId);
  }

  // Recuperar round_id
  Future<String?> retrieveRoundId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(roundIdKey);
  }

  // Recuperar user_id
  Future<String?> retrieveUserId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(userIdKey);
  }

  // Salvar valor do dado
  Future<void> storeDiceValue(int diceValue) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(diceValueKey, diceValue);
  }

  // Recuperar valor do dado
  Future<int?> retrieveDiceValue() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt(diceValueKey);
  }

  // Limpar tudo
  Future<void> clearAll() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(roundIdKey);
    await prefs.remove(userIdKey);
    await prefs.remove(diceValueKey);
  }
}
