<!DOCTYPE html>
<html>
<head>
  <title>Face Detection and Recognition with FaceAPI.js</title>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.1/dist/tf.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@vladmandic/face-api/dist/face-api.min.js"></script>
  <style>
    canvas {
      position: absolute;
      top: 0;
      left: 0;
    }
  </style>
</head>
<body>
  <img id="image" src="https://example.com/image.jpg" />
  <canvas id="myCanvas"></canvas>

  <script>
    // Tải các mô hình học máy
    Promise.all([
      faceapi.nets.ssdMobilenetv1.loadFromUri('/models'),
      faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
      faceapi.nets.faceRecognitionNet.loadFromUri('/models')
    ]).then(startProcessing);

    async function startProcessing() {
      const image = document.getElementById('image');
      const canvas = document.getElementById('myCanvas');
      canvas.width = image.width;
      canvas.height = image.height;

      // Phát hiện khuôn mặt
      const detections = await faceapi.detectAllFaces(image, new faceapi.SsdMobilenetv1Options());

      // Nhận dạng khuôn mặt
      const labeledFaceDescriptors = await loadFaceDescriptors();
      const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);
      const results = detections.map(det => faceMatcher.findBestMatch(det.descriptor));

      // Vẽ kết quả lên canvas
      const displaySize = { width: image.width, height: image.height };
      faceapi.matchDimensions(canvas, displaySize);

      const resizedDetections = faceapi.resizeResults(detections, displaySize);
      const resizedResults = faceapi.resizeResults(results, displaySize);

      const drawOptions = {
        lineWidth: 2,
        boxColor: 'green',
        textColor: 'green'
      };

      faceapi.draw.drawDetections(canvas, resizedDetections);
      faceapi.draw.drawFaceLabels(canvas, resizedResults, drawOptions);
    }

    async function loadFaceDescriptors() {
      // Đọc dữ liệu mô tả khuôn mặt từ file hoặc API
      return [
        new faceapi.LabeledFaceDescriptors('Person 1', [descriptor1]),
        new faceapi.LabeledFaceDescriptors('Person 2', [descriptor2]),
        // Thêm các mô tả khuôn mặt khác vào đây
      ];
    }
  </script>
</body>
</html>