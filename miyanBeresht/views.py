# miyanBeresht/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import BereshtMenu, BereshtMenuItem
from .serializers import BereshtMenuSerializer, BereshtMenuItemSerializer


class BereshtMenuViewSet(BaseMenuViewSet):
    """API endpoint for Beresht menus."""

    queryset = BereshtMenu.objects.select_related('branch').filter(branch__code='beresht').prefetch_related('sections__items')
    serializer_class = BereshtMenuSerializer


class BereshtMenuItemViewSet(BaseMenuItemViewSet):
    """API endpoint for Beresht menu items."""

    queryset = BereshtMenuItem.objects.filter(section__menu__branch__code='beresht')
    serializer_class = BereshtMenuItemSerializer


from django.http import HttpResponse
from rest_framework.views import APIView


class FlameMonitorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Flame Monitor</title>

<style>
body {
  margin: 0;
  background: #000;
  color: #0f0;
  font-family: system-ui, sans-serif;
}
video {
  width: 100vw;
}
#ui {
  position: fixed;
  bottom: 0;
  width: 100%;
  background: rgba(0,0,0,0.85);
  padding: 10px;
}
button {
  width: 100%;
  padding: 10px;
  background: #111;
  color: #0f0;
  border: 1px solid #0f0;
}
.row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}
canvas {
  width: 100%;
  height: 120px;
  background: #020;
  margin-top: 6px;
}
</style>
</head>

<body>

<video id="video" playsinline muted></video>

<div id="ui">
  <button id="start">Start Monitoring</button>
  <div class="row"><span>Blue fraction</span><span id="val">–</span></div>
  <canvas id="chart" width="600" height="120"></canvas>
</div>
<script>
(() => {
  const video = document.getElementById("video");
  const startBtn = document.getElementById("start");
  const valEl = document.getElementById("val");

  const chart = document.getElementById("chart");
  const gctx = chart.getContext("2d");

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d", { willReadFrequently: true });

  const history = [];
  const MAX_POINTS = 200;

  async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: { exact: "environment" },
        width: { ideal: 640 },
        height: { ideal: 480 },
        frameRate: { ideal: 30 }
      },
      audio: false
    });

    video.srcObject = stream;
    await video.play();

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    requestAnimationFrame(loop);
  }

  function loop() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

    let sumY = 0;
    let countY = 0;

    // First pass: mean intensity
    for (let i = 0; i < data.length; i += 4) {
      const Y = data[i] + data[i+1] + data[i+2];
      sumY += Y;
      countY++;
    }

    const meanY = sumY / countY;

    let flameSum = 0;
    let flameCount = 0;

    // Second pass: positive normalized deviation
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];

      const Y = r + g + b;
      const yNorm = Y / meanY;

      // Flame-like condition (very loose)
      if (yNorm > 1.15) {
        flameSum += (yNorm - 1);
        flameCount++;
      }
    }

    if (flameCount > 100) {
      const FED = flameSum / flameCount;
      valEl.textContent = FED.toFixed(4);

      history.push(FED);
      if (history.length > MAX_POINTS) history.shift();

      drawChart();
    }

    requestAnimationFrame(loop);
  }

  function drawChart() {
    gctx.clearRect(0, 0, chart.width, chart.height);

    const min = Math.min(...history);
    const max = Math.max(...history);
    const range = (max - min) || 1;

    gctx.strokeStyle = "#0f0";
    gctx.beginPath();

    history.forEach((v, i) => {
      const x = i * chart.width / MAX_POINTS;
      const y = chart.height - ((v - min) / range) * chart.height;
      if (i === 0) gctx.moveTo(x, y);
      else gctx.lineTo(x, y);
    });

    gctx.stroke();
  }

  startBtn.onclick = () => {
    startBtn.disabled = true;
    startCamera().catch(e => alert(e.message));
  };
})();
</script>


</body>
</html>
"""
        return HttpResponse(html, content_type="text/html; charset=utf-8")
