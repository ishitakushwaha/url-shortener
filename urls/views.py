from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import redirect
from django.http import HttpResponseGone, HttpResponseNotFound
from django.utils import timezone
from datetime import timedelta

from .models import ShortURL
from .serializers import CreateShortURLSerializer
from .utils import generate_short_code

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
@method_decorator(csrf_exempt, name="dispatch")
class CreateShortURLView(APIView):

    def post(self, request):
        serializer = CreateShortURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        short_code = data.get("custom_alias") or generate_short_code()

        expires_at = data.get("expiration_date")
        if expires_at is None:
            expires_at = timezone.now() + timedelta(
                days=settings.DEFAULT_URL_EXPIRATION_DAYS
            )

        for _ in range(5):
            try:
                obj = ShortURL.objects.create(
                    short_code=short_code,
                    long_url=data["long_url"],
                    expires_at=expires_at,  # ✅ FIXED
                )
                break
            except IntegrityError:
                if data.get("custom_alias"):
                    return Response(
                        {"error": "Custom alias already exists"},
                        status=status.HTTP_409_CONFLICT,
                    )
                short_code = generate_short_code()
        else:
            return Response(
                {"error": "Failed to generate short code"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "short_url": f"{settings.BASE_URL}/{obj.short_code}",
                "expires_at": obj.expires_at,
            },
            status=status.HTTP_201_CREATED,
        )

class RedirectShortURLView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_code):
        try:
            obj = ShortURL.objects.get(short_code=short_code)
        except ShortURL.DoesNotExist:
            return HttpResponseNotFound()

        if obj.is_expired():
            return HttpResponseGone()

        return redirect(obj.long_url, permanent=False)
