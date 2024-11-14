# user/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from app.middleware import failure_response
from .models import User
from .serializers import UserSerializer

# Get all users
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all_users(request):
    users = User.objects.filter(deleted=False)
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)

# Get user by id
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user(request, id):
    if id is None:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        user = User.objects.get(id=id, deleted=False)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
   
    serializer = UserSerializer(user, context={'request': request})
    
    
    return Response(serializer.data)


# Create a new user
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update an existing user
@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_user(request, id):
    try:
        user = User.objects.get(id=id, deleted=False)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete ủe
@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_user(request, id):
    try:
        user = User.objects.get(id=id, deleted=False)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    user.deleted = True
    user.deleted_at = timezone.now()
    user.save()
    return Response({"message": "User has been soft-deleted."}, status=status.HTTP_204_NO_CONTENT)
