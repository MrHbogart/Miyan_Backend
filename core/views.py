from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


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


class StaffLinkAPIView(APIView):
    """Link a staff profile (by bot_token) to a telegram_id and return DRF token."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = serializers.StaffLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bot_token = serializer.validated_data['bot_token']
        telegram_id = serializer.validated_data['telegram_id']

        try:
            profile = models.StaffProfile.objects.get(bot_token=bot_token)
        except models.StaffProfile.DoesNotExist:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        profile.telegram_id = str(telegram_id)
        profile.save()

        # Ensure the user has an auth token
        token, _ = Token.objects.get_or_create(user=profile.user)

        return Response({'token': token.key, 'username': profile.user.username})


class TokenByTelegramAPIView(APIView):
    """Return DRF token for a telegram_id when called by the trusted bot using the shared secret."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        secret = request.headers.get('X-BOT-SECRET') or request.data.get('secret')
        if not secret or secret != getattr(settings, 'BOT_SHARED_SECRET', ''):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        telegram_id = str(request.data.get('telegram_id') or request.query_params.get('telegram_id') or '')
        if not telegram_id:
            return Response({'detail': 'telegram_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = models.StaffProfile.objects.get(telegram_id=telegram_id)
        except models.StaffProfile.DoesNotExist:
            return Response({'detail': 'Not linked'}, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=profile.user)
        return Response({'token': token.key})


class StaffProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for managing staff profiles"""
    queryset = models.StaffProfile.objects.all()
    serializer_class = serializers.StaffProfileSerializer
    permission_classes = [IsAuthenticated]
