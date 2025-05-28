import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(AIWriterApp());

class AIWriterApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Writer',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: AIWriterHomePage(),
    );
  }
}

class AIWriterHomePage extends StatefulWidget {
  @override
  _AIWriterHomePageState createState() => _AIWriterHomePageState();
}

class _AIWriterHomePageState extends State<AIWriterHomePage> {
  final TextEditingController _controller = TextEditingController();
  String _result = '';
  bool _loading = false;

  Future<void> _generateText() async {
    setState(() => _loading = true);
    final url = Uri.parse('http://10.0.2.2:8000/generate'); // Use 10.0.2.2 for Android emulator, localhost for web/desktop
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'prompt': _controller.text}),
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      setState(() => _result = jsonDecode(response.body)['result']);
    } else {
      setState(() => _result = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Writer')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(labelText: 'Enter your prompt'),
              minLines: 1,
              maxLines: 5,
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loading ? null : _generateText,
              child: _loading ? CircularProgressIndicator() : Text('Generate'),
            ),
            SizedBox(height: 24),
            Expanded(
              child: SingleChildScrollView(
                child: Text(_result, style: TextStyle(fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
