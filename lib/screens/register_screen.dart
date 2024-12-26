import 'package:flutter/material.dart';
import 'package:royal_ai/screens/login_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  void _register() {
    // Logic register bisa ditambahkan di sini (misalnya memverifikasi kredensial)
    print('Email: ${_emailController.text}');
    print('Password: ${_passwordController.text}');
    print('Confirm Password: ${_confirmPasswordController.text}');
    // Setelah register berhasil, bisa menavigasi ke halaman login atau home
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => LoginScreen()),
    ); // Ganti dengan nama rute yang sesuai
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Image.asset(
              'assets/images/royal_logo.png',
              height: 200, // Atur ukuran gambar sesuai kebutuhan
              width: 200, // Atur ukuran gambar sesuai kebutuhan
            ),
            const SizedBox(
                height: 20), // Memberikan jarak antara gambar dan form
            // Email TextField
            TextField(
              controller: _emailController,
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                  borderSide: BorderSide(color: Theme.of(context).primaryColor),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                  borderSide: BorderSide(color: Colors.grey),
                ),
              ),
              keyboardType: TextInputType.emailAddress,
            ),
            const SizedBox(height: 16.0),

            // Password TextField
            TextField(
              controller: _passwordController,
              decoration: InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                  borderSide: BorderSide(color: Theme.of(context).primaryColor),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                  borderSide: BorderSide(color: Colors.grey),
                ),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 16.0),

            // Confirm Password TextField
            TextField(
              controller: _confirmPasswordController,
              decoration: InputDecoration(
                labelText: 'Confirm Password',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                  borderSide: BorderSide(color: Theme.of(context).primaryColor),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8.0),
                  borderSide: BorderSide(color: Colors.grey),
                ),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 20.0),

            // Register Button
            SizedBox(
              width: double.infinity,
              height: 50, // Tombol akan mengisi lebar penuh
              child: ElevatedButton(
                onPressed: _register,
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(
                        8.0), // Border kotak dengan radius sudut
                  ),
                  side: BorderSide(
                      color: Theme.of(context).primaryColor), // Border color
                ),
                child: const Text('Register'),
              ),
            ),
            const SizedBox(height: 10.0),

            // Navigate to Login Screen
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => LoginScreen()),
                );
              },
              child: const Text('Already have an account? Login here'),
            ),
          ],
        ),
      ),
    );
  }
}
