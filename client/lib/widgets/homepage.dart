import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

String selectedItem = "144p";

class DropDownResolution extends StatefulWidget {
  const DropDownResolution({super.key});

  @override
  State<DropDownResolution> createState() => _DropDownResolutionState();
}

class HomePage extends StatelessWidget {
  final formInputController = TextEditingController();

  HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AllInOne Downloader'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 50),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Paste the link below for the video',
                style: TextStyle(
                  fontSize: 20,
                ),
              ),
              const SizedBox(
                height: 30.0,
              ),
              TextFormField(
                decoration: const InputDecoration(
                  labelText: 'paste your link',
                  border: OutlineInputBorder(),
                ),
                controller: formInputController,
              ),
              const SizedBox(
                height: 20.0,
              ),
              const SizedBox(
								height: 50.0,
                child: DropDownResolution(),
              ),
              const SizedBox(
                height: 30.0,
              ),
              TextButton(
                style: TextButton.styleFrom(
                  foregroundColor: Colors.white,
                  backgroundColor: Colors.blue,
									fixedSize: const Size(100.0, 40.0)
                ),
                onPressed: () async {
                  // print(formInputController.text);
                  Map ytUrlData = {
                    'url': formInputController.text,
                    'resolution': selectedItem,
                  };

                  // encode map to json
                  var body = json.encode(ytUrlData);

                  // for android emulator
                  // String serverUrl = 'http://10.0.2.2:5000/download';
                  String serverUrl = 'http://localhost:5000/download';

                  final response = await http.post(Uri.parse(serverUrl),
                      headers: {"Content-Type": "application/json"},
                      body: body);

                  if (response.statusCode == 200) {
                    var data = json.decode(response.body);
                    // print(data);
                  } else {
                    throw Exception("Failed to load entry...");
                  }
                },
                child: const Text('Download'),
              )
            ],
          ),
        ),
      ),
    );
  }
}

class _DropDownResolutionState extends State<DropDownResolution> {
  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      value: "1080p",
      items: <String>['144p', '240p', '360p', '480p', '720p', '1080p'].map((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
      onChanged: (String? newValue) {
        setState(() {
          selectedItem = newValue!;
        });
      },
			decoration: const InputDecoration(
				border: OutlineInputBorder(),
			),
    );
  }
}
