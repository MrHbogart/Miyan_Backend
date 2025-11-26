from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthcheckView(APIView):
    """Lightweight endpoint for load balancers and uptime monitors."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = []

    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'timestamp': timezone.now().isoformat(),
                'version': settings.APP_VERSION,
                'revision': settings.APP_COMMIT_SHA,
            }
        )
