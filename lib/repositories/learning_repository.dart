import '../models/learning_entry.dart';

class LearningRepository {
  // Temporary in-memory storage
  final List<LearningEntry> _entries = [];

  Future<List<LearningEntry>> getAll() async {
    return _entries;
  }

  Future<LearningEntry?> getById(String id) async {
    try {
      return _entries.firstWhere((e) => e.id == id);
    } catch (_) {
      return null;
    }
  }

  Future<void> create(LearningEntry entry) async {
    _entries.add(entry);
  }

  Future<void> update(LearningEntry entry) async {
    final index = _entries.indexWhere((e) => e.id == entry.id);
    if (index != -1) {
      _entries[index] = entry;
    }
  }

  Future<void> delete(String id) async {
    _entries.removeWhere((e) => e.id == id);
  }

  Future<List<LearningEntry>> search(String query) async {
    return _entries.where((e) {
      return e.title.toLowerCase().contains(query.toLowerCase()) || 
             e.content.toLowerCase().contains(query.toLowerCase());
    }).toList();
  }
}
