// This is the camera test screen
// We display the camera feed here
// We also display the buttons to take a picture and to switch between front and back camera

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:opencv_4/opencv_4.dart';

class CameraTest extends StatefulWidget {
  const CameraTest({Key? key}) : super(key: key);

  @override
  State<CameraTest> createState() => _CameraTestState();
}

class _CameraTestState extends State<CameraTest> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Camera Test'),
      ),
      body: Column(
        children: [
          Expanded(
            child: _buildCameraFeed(),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              ElevatedButton(
                onPressed: _switchCamera,
                child: const Text('Switch Camera'),
              ),
              ElevatedButton(
                onPressed: _takePicture,
                child: const Text('Take Picture'),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _cameraFeed = const Text('Camera feed goes here');
  CameraController? _cameraController;
  bool _isCameraInitialized = false;
  bool _isCameraFront = true;
  // This is the camera feed
  // We display the camera feed here

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  void _initializeCamera() async {
    final cameras = await availableCameras();
    final camera = cameras.first;
    _cameraController = CameraController(camera, ResolutionPreset.medium);
    await _cameraController!.initialize();
    setState(() {
      _isCameraInitialized = true;
    });
  }

  void _switchCamera() {
    if (_isCameraInitialized) {
      _cameraController!.dispose();
      _isCameraFront = !_isCameraFront;
      _initializeCamera();
    }
  }

  void _takePicture() async {}

  // This is the camera feed
  // We display the camera feed here
  Widget _buildCameraFeed() {
    if (_isCameraInitialized) {
      return AspectRatio(
        aspectRatio: _cameraController!.value.aspectRatio,
        child: CameraPreview(_cameraController!),
      );
    } else {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }
  }
}
