import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';

import 'package:royal_ai/screens/home_screen.dart';

import '../provider/settings_provider.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({Key? key}) : super(key: key);

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();

    // Timer untuk pindah ke HomeScreen setelah 3 detik
    Timer(const Duration(seconds: 3), () {
      Navigator.pushReplacement(
          context, MaterialPageRoute(builder: (context) => const HomeScreen()));
    });
  }

  @override
  Widget build(BuildContext context) {
    // Menyesuaikan tema dari SettingsProvider
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
          ],
        ),
      ),
    );
  }
}