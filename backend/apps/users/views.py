from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserMeView(APIView):
    # def get() will called when someone ask for user data throught api like... GET /api/v1/users/me/
    def get(self, request):
        user = User.objects.first()
        if not user:
            return Response(
                {"message": "No users found."},
                status=404,
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)
