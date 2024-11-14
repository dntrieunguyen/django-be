from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'avatar_url',
            'created_at', 'updated_at', 'deleted', 'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']