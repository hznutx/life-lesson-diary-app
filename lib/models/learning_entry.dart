class LearningEntry {
  final String id;
  final DateTime date;
  final String title;
  final String content;
  final String? reflection;
  final List<String> tags;
  final DateTime createdAt;
  final DateTime updatedAt;

  const LearningEntry({
    required this.id,
    required this.date,
    required this.title,
    required this.content,
    this.reflection,
    this.tags = const [],
    required this.createdAt,
    required this.updatedAt,
  });
}
