# miyanBeresht/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import (
    BereshtMenu, BereshtMenuItem,
    BereshtInventoryItem, BereshtInventoryRecord
)
from .serializers import (
    BereshtMenuSerializer, BereshtMenuItemSerializer,
    BereshtInventoryItemSerializer, BereshtInventoryRecordSerializer
)


class BereshtMenuViewSet(BaseMenuViewSet):
    """API endpoint for Beresht menus."""

    queryset = BereshtMenu.objects.all().prefetch_related('sections__items')
    serializer_class = BereshtMenuSerializer


class BereshtMenuItemViewSet(BaseMenuItemViewSet):
    """API endpoint for Beresht menu items."""

    queryset = BereshtMenuItem.objects.all()
    serializer_class = BereshtMenuItemSerializer


class BereshtInventoryItemViewSet(ReadOnlyModelViewSet):
    """API endpoint for Beresht inventory items."""
    queryset = BereshtInventoryItem.objects.all()
    serializer_class = BereshtInventoryItemSerializer
    permission_classes = [AllowAny]


class BereshtInventoryRecordViewSet(viewsets.ModelViewSet):
    """API endpoint for Beresht inventory records."""
    queryset = BereshtInventoryRecord.objects.all()
    serializer_class = BereshtInventoryRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class FlameMonitorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        html = """
<!DOCTYPE html>
<html lang="en">
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
      height: auto;
    }
    #ui {
      position: fixed;
      bottom: 0;
      width: 100%;
      padding: 12px;
      background: rgba(0,0,0,0.8);
      box-sizing: border-box;
    }
    .row {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
    }
    button {
      width: 100%;
      padding: 12px;
      margin-bottom: 6px;
      background: #111;
      color: #0f0;
      border: 1px solid #0f0;
      font-size: 16px;
    }
  </style>
</head>

<body>
  <video id="video" playsinline muted></video>

  <div id="ui">
    <button id="start">Start Flame Monitoring</button>
    <div class="row"><span>Brightness</span><span id="b">–</span></div>
    <div class="row"><span>Δ Brightness</span><span id="db">–</span></div>
    <div class="row"><span>Color Ratio</span><span id="c">–</span></div>
  </div>

  <script src="/static/flame.js"></script>
</body>
</html>
        """

        response = HttpResponse(html, content_type="text/html; charset=utf-8")
        response["Cache-Control"] = "no-store"
        return response
