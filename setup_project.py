import os

project_dir = "/Users/hzn/Documents/GitHub/diary-life-lesson-app"

dirs = [
    "lib/app",
    "lib/core/constants",
    "lib/core/database",
    "lib/core/theme",
    "lib/core/utils",
    "lib/models",
    "lib/repositories",
    "lib/screens/home",
    "lib/screens/history",
    "lib/screens/entry",
    "lib/screens/settings",
    "lib/widgets",
    "test",
    "ios",
    "android"
]

for d in dirs:
    os.makedirs(os.path.join(project_dir, d), exist_ok=True)

files = {
    "pubspec.yaml": """name: learning_journal
description: "A simple personal Learning Journal mobile app using Flutter."
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
""",
    "lib/main.dart": """import 'package:flutter/material.dart';
import 'app/app.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const LearningJournalApp());
}
""",
    "lib/app/app.dart": """import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/constants/app_constants.dart';
import '../screens/home/home_screen.dart';
import '../screens/history/history_screen.dart';
import '../screens/settings/settings_screen.dart';
import '../screens/entry/entry_form_screen.dart';
import '../screens/entry/entry_detail_screen.dart';

class LearningJournalApp extends StatelessWidget {
  const LearningJournalApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.system,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/history': (context) => const HistoryScreen(),
        '/settings': (context) => const SettingsScreen(),
        '/entry': (context) => const EntryFormScreen(),
        '/entry/detail': (context) => const EntryDetailScreen(),
      },
    );
  }
}
""",
    "lib/app/routes.dart": """class AppRoutes {
  static const home = '/';
  static const history = '/history';
  static const settings = '/settings';
  static const entry = '/entry';
  static const entryDetail = '/entry/detail';
}
""",
    "lib/core/theme/app_theme.dart": """import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get light {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.teal,
        brightness: Brightness.light,
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: false,
        elevation: 0,
      ),
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.grey.shade200),
        ),
      ),
    );
  }

  static ThemeData get dark {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.teal,
        brightness: Brightness.dark,
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: false,
        elevation: 0,
      ),
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.grey.shade800),
        ),
      ),
    );
  }
}
""",
    "lib/core/constants/app_constants.dart": """class AppConstants {
  static const appName = 'Life Lesson Diary';
}
""",
    "lib/core/utils/date_utils.dart": """class AppDateUtils {
  static String getGreeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) {
      return 'Good morning 👋';
    } else if (hour < 17) {
      return 'Good afternoon 👋';
    } else {
      return 'Good evening 👋';
    }
  }

  static String formatDate(DateTime date) {
    const months = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    return '${months[date.month - 1]} ${date.day}, ${date.year}';
  }
}
""",
    "lib/core/database/database.dart": """// TODO: Implement SQLite database connection and initialization in the next milestone.
// This file is currently a placeholder for the local persistence layer.
""",
    "lib/models/learning_entry.dart": """class LearningEntry {
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
""",
    "lib/repositories/learning_repository.dart": """import '../models/learning_entry.dart';

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
""",
    "lib/screens/home/home_screen.dart": """import 'package:flutter/material.dart';
import '../../core/utils/date_utils.dart';
import '../../widgets/app_bottom_navigation.dart';
import '../../widgets/learning_card.dart';
import '../../widgets/empty_state.dart';
import '../../models/learning_entry.dart';
import '../../repositories/learning_repository.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _repository = LearningRepository();
  List<LearningEntry> _entries = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadEntries();
  }

  Future<void> _loadEntries() async {
    final entries = await _repository.getAll();
    setState(() {
      _entries = entries;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),
              Text(
                AppDateUtils.getGreeting(),
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'What did you learn today?',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: Colors.grey.shade600,
                ),
              ),
              const SizedBox(height: 24),
              InkWell(
                onTap: () {
                  Navigator.pushNamed(context, '/entry').then((_) => _loadEntries());
                },
                borderRadius: BorderRadius.circular(16),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(vertical: 24),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primaryContainer,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.add,
                        color: Theme.of(context).colorScheme.onPrimaryContainer,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        "Add today's learning",
                        style: TextStyle(
                          color: Theme.of(context).colorScheme.onPrimaryContainer,
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 32),
              Text(
                'Recent',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: _isLoading 
                  ? const Center(child: CircularProgressIndicator())
                  : _entries.isEmpty 
                    ? EmptyState(
                        message: 'No learning entries yet.\\n\\nStart by writing down\\nwhat you learned today.',
                        buttonText: 'Add your first learning',
                        onButtonPressed: () {
                          Navigator.pushNamed(context, '/entry').then((_) => _loadEntries());
                        },
                      )
                    : ListView.builder(
                        itemCount: _entries.length,
                        itemBuilder: (context, index) {
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 12.0),
                            child: LearningCard(entry: _entries[index]),
                          );
                        },
                      ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: const AppBottomNavigation(currentIndex: 0),
    );
  }
}
""",
    "lib/screens/history/history_screen.dart": """import 'package:flutter/material.dart';
import '../../widgets/app_bottom_navigation.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('History'),
      ),
      body: const Center(
        child: Text(
          'Your learning history\\nwill appear here.',
          textAlign: TextAlign.center,
        ),
      ),
      bottomNavigationBar: const AppBottomNavigation(currentIndex: 1),
    );
  }
}
""",
    "lib/screens/settings/settings_screen.dart": """import 'package:flutter/material.dart';
import '../../widgets/app_bottom_navigation.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: const Center(
        child: Text(
          'Settings will be available here.',
          textAlign: TextAlign.center,
        ),
      ),
      bottomNavigationBar: const AppBottomNavigation(currentIndex: 2),
    );
  }
}
""",
    "lib/screens/entry/entry_form_screen.dart": """import 'package:flutter/material.dart';
import '../../core/utils/date_utils.dart';

class EntryFormScreen extends StatefulWidget {
  const EntryFormScreen({super.key});

  @override
  State<EntryFormScreen> createState() => _EntryFormScreenState();
}

class _EntryFormScreenState extends State<EntryFormScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('New Learning'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Date',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 8),
            Text(
              AppDateUtils.formatDate(DateTime.now()),
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 24),
            Text(
              'What did you learn?',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                hintText: 'A short title...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Tell me more',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 8),
            const TextField(
              maxLines: 5,
              decoration: InputDecoration(
                hintText: 'Elaborate on the topic...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'What is still unclear?',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 8),
            const TextField(
              maxLines: 3,
              decoration: InputDecoration(
                hintText: 'Questions for future...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Tags',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                hintText: 'e.g. flutter, dart, architecture',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  // TODO: Implement actual save logic
                  Navigator.pop(context);
                },
                child: const Text('Save Learning'),
              ),
            ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}
""",
    "lib/screens/entry/entry_detail_screen.dart": """import 'package:flutter/material.dart';

class EntryDetailScreen extends StatelessWidget {
  const EntryDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Entry Detail'),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit),
            onPressed: () {
              // TODO: Navigate to edit form
            },
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Title placeholder',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(
              'Sep 24, 2026',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Content placeholder. This is where the details of the learning entry will be displayed.',
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 24),
            Text(
              'Reflection',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Reflection placeholder. Things that are still unclear.',
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 24),
            const Wrap(
              spacing: 8,
              children: [
                Chip(label: Text('#flutter')),
                Chip(label: Text('#dart')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
""",
    "lib/widgets/app_bottom_navigation.dart": """import 'package:flutter/material.dart';
import '../app/routes.dart';

class AppBottomNavigation extends StatelessWidget {
  final int currentIndex;

  const AppBottomNavigation({
    super.key,
    required this.currentIndex,
  });

  @override
  Widget build(BuildContext context) {
    return NavigationBar(
      selectedIndex: currentIndex,
      onDestinationSelected: (index) {
        if (index == currentIndex) return;
        
        String route;
        switch (index) {
          case 0:
            route = AppRoutes.home;
            break;
          case 1:
            route = AppRoutes.history;
            break;
          case 2:
            route = AppRoutes.settings;
            break;
          default:
            route = AppRoutes.home;
        }
        
        Navigator.pushReplacementNamed(context, route);
      },
      destinations: const [
        NavigationDestination(
          icon: Icon(Icons.home_outlined),
          selectedIcon: Icon(Icons.home),
          label: 'Home',
        ),
        NavigationDestination(
          icon: Icon(Icons.history_outlined),
          selectedIcon: Icon(Icons.history),
          label: 'History',
        ),
        NavigationDestination(
          icon: Icon(Icons.settings_outlined),
          selectedIcon: Icon(Icons.settings),
          label: 'Settings',
        ),
      ],
    );
  }
}
""",
    "lib/widgets/learning_card.dart": """import 'package:flutter/material.dart';
import '../models/learning_entry.dart';
import '../core/utils/date_utils.dart';

class LearningCard extends StatelessWidget {
  final LearningEntry entry;

  const LearningCard({
    super.key,
    required this.entry,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(context, '/entry/detail');
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                entry.title,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 4),
              Text(
                entry.content,
                style: Theme.of(context).textTheme.bodyMedium,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    AppDateUtils.formatDate(entry.date),
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey,
                    ),
                  ),
                  if (entry.tags.isNotEmpty)
                    Text(
                      entry.tags.map((t) => '#$t').join(' '),
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: Colors.grey,
                      ),
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
""",
    "lib/widgets/empty_state.dart": """import 'package:flutter/material.dart';

class EmptyState extends StatelessWidget {
  final String message;
  final String buttonText;
  final VoidCallback onButtonPressed;

  const EmptyState({
    super.key,
    required this.message,
    required this.buttonText,
    required this.onButtonPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.book_outlined,
            size: 64,
            color: Colors.grey.shade400,
          ),
          const SizedBox(height: 24),
          Text(
            message,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: Colors.grey.shade600,
            ),
          ),
          const SizedBox(height: 32),
          ElevatedButton(
            onPressed: onButtonPressed,
            child: Text(buttonText),
          ),
        ],
      ),
    );
  }
}
""",
    "README.md": """# Life Lessons Diary

## Project

Learning Journal is a personal offline-first Flutter application for recording what was learned each day.

## Current milestone

* Flutter project initialized
* App architecture created
* Material 3 theme
* Home screen
* Bottom navigation
* Entry form UI
* History placeholder
* Settings placeholder
* Local repository abstraction

## Future milestones

### Phase 2 — Persistence
* SQLite
* Create entry
* Edit entry
* Delete entry
* Load history

### Phase 3 — Productivity
* Search
* Tags
* Calendar
* Filtering

### Phase 4 — Personalization
* Dark mode improvements
* App icon
* Notifications
* Face ID

### Phase 5 — Backup
* Export JSON
* Import JSON
* Markdown export
* iCloud backup consideration
"""
}

for path, content in files.items():
    with open(os.path.join(project_dir, path), "w") as f:
        f.write(content)
print("Files created successfully.")
