import 'package:flutter_test/flutter_test.dart';

import 'package:learning_journal/app/app.dart';

void main() {
  testWidgets('App launches successfully', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const LearningJournalApp());

    // Verify that the Home screen is shown
    expect(find.text('What did you learn today?'), findsOneWidget);
  });
}
