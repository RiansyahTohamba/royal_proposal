import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:provider/provider.dart';
import 'package:royal_ai/provider/chat_provider.dart';
import 'package:royal_ai/provider/settings_provider.dart';
import 'package:royal_ai/screens/home_screen.dart';
import 'package:royal_ai/screens/login_screen.dart';
import 'package:royal_ai/screens/onboarding_screen.dart';
import 'package:royal_ai/screens/splash_screen.dart';
import 'package:royal_ai/themes/my_theme.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
   final prefs = await SharedPreferences.getInstance();

  await dotenv.load(fileName: ".env");

  await ChatProvider.initHive();

  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (context) => ChatProvider()),
      ChangeNotifierProvider(create: (context) => SettingsProvider()),
    ],
    child: MyApp(prefs:prefs ,),
  ));
}

class MyApp extends StatefulWidget {
  final SharedPreferences prefs;
  MyApp({super.key, required this.prefs});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    setTheme();
    super.initState();
  }

  void setTheme() {
    final settingsProvider = context.read<SettingsProvider>();
    settingsProvider.getSavedSettings();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
  theme: context.watch<SettingsProvider>().isDarkMode ? darkTheme : lightTheme,
  debugShowCheckedModeBanner: false,
  initialRoute: '/',
  routes: {
    '/': (context) => SplashScreen(prefs: widget.prefs),
    '/onboarding': (context) => OnboardingScreen(),
    '/home': (context) => LoginScreen(),
  },
);

  }
}
