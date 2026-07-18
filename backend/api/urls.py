from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request):
        return Response({
            "status": "healthy",
            "service": "PRPilot API",
            "version": "1.0.0"
        })


urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("users/", include("apps.users.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("repositories/", include("apps.repositories.urls")),
    path("pull-req/", include("apps.reviews.urls"))
]
