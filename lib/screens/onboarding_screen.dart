import 'package:flutter/material.dart';
import 'package:introduction_screen/introduction_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'home_screen.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({Key? key}) : super(key: key);

  Future<void> _completeOnboarding(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('onboarding_completed', true);
    Navigator.pushReplacement(
    context,
    MaterialPageRoute(builder: (context) => HomeScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IntroductionScreen(
        pages: [
          PageViewModel(
            title: "Selamat Datang!",
            body: "Temukan fitur canggih dengan aplikasi ini.",
            image: Center(child: Image.asset("assets/images/onboarding1.png", height: 200)),
            decoration: const PageDecoration(
              bodyTextStyle: TextStyle(fontSize: 16),
              titleTextStyle: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ),
          PageViewModel(
            title: "AI Cerdas",
            body: "Rasakan kemudahan dengan teknologi AI.",
            image: Center(child: Image.asset("assets/images/onboarding2.png", height: 200)),
          ),
          PageViewModel(
            title: "Mari Mulai",
            body: "Klik tombol selesai untuk mulai!",
            image: Center(child: Image.asset("assets/images/onboarding3.png", height: 200)),
          ),
        ],
        onDone: () => _completeOnboarding(context),
        showSkipButton: true,
        skip: const Text("Lewati"),
        next: const Icon(Icons.arrow_forward),
        done: const Text("Selesai", style: TextStyle(fontWeight: FontWeight.w600)),
        dotsDecorator: const DotsDecorator(
          size: Size(10.0, 10.0),
          color: Colors.grey,
          activeSize: Size(22.0, 10.0),
          activeColor: Colors.blue,
          spacing: EdgeInsets.symmetric(horizontal: 4),
          activeShape: RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(25.0)),
          ),
        ),
      ),
    );
  }
}
