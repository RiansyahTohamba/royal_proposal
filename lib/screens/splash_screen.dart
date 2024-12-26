import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';

import 'package:shared_preferences/shared_preferences.dart';

import '../provider/settings_provider.dart';


class SplashScreen extends StatefulWidget {
  final SharedPreferences prefs; // Tambah parameter prefs

  const SplashScreen({super.key, required this.prefs});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    navigateToNextScreen(); // Pindah ke halaman berikutnya
  }

  void navigateToNextScreen() async {
    bool? completed = widget.prefs.getBool('onboarding_completed') ?? false;

    await Future.delayed(const Duration(seconds: 1));

    if (completed) {
      Navigator.pushReplacementNamed(context, '/home'); // Jika onboarding selesai
    } else {
      Navigator.pushReplacementNamed(context, '/onboarding'); // Jika belum
    }
  }

  @override
  Widget build(BuildContext context) {
     final isDarkMode = context.watch<SettingsProvider>().isDarkMode;
    return Scaffold(
            backgroundColor: isDarkMode ? Colors.black : Colors.white, // Warna latar belakang sesuai tema

      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              isDarkMode ? 'assets/images/royal_logo.png' : 'assets/images/royal_logo.png', // Logo sesuai tema
              height: 200,
            ),
            const SizedBox(height: 20),
            const CircularProgressIndicator(), // Animasi loading
          ],
        ),
      ),
    );
  }
}
