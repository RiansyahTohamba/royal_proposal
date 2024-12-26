import 'package:flutter/material.dart';
import 'package:royal_ai/screens/home_screen.dart';
import 'package:royal_ai/screens/register_screen.dart'; // Pastikan untuk mengganti import sesuai struktur proyek Anda

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  void _login() {
    // Logic login bisa ditambahkan di sini (misalnya memverifikasi kredensial)
    print('Email: ${_emailController.text}');
    print('Password: ${_passwordController.text}');
    // Setelah login berhasil, bisa menavigasi ke halaman utama
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => HomeScreen()),
    ); // Ganti dengan nama rute yang sesuai
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            Image.asset(
              'assets/images/royal_logo.png',
              height: 200, // Atur ukuran gambar sesuai kebutuhan
              width: 200, // Atur ukuran gambar sesuai kebutuhan
            ),
            SizedBox(height: 20), // Memberikan jarak antara gambar dan form
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
            SizedBox(height: 16.0),

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
            SizedBox(
              height: 20.0,
            ),
            SizedBox(
              width: double.infinity,
              height: 50, // Tombol akan mengisi lebar penuh
              child: ElevatedButton(
                onPressed: _login,
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(
                        8.0), // Border kotak dengan radius sudut
                  ),
                  side: BorderSide(
                      color: Theme.of(context).primaryColor), // Border color
                ),
                child: Text('Login'),
              ),
            ),
            SizedBox(
              height: 10.0,
            ),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => RegisterScreen()),
                );
              },
              child: Text('Don\'t have an account? Register here'),
            ),
          ],
        ),
      ),
    );
  }
}
