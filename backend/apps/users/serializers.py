from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )
# browser cannot understand the python object, so we have to conevrt it into json. serializer is used for it.
# A serializer converts Django model instances into JSON for API responses and can also validate incoming JSON before creating or updating model instances.
