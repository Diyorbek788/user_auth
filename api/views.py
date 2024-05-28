from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from app_main.models import Note  # Note modelini to'g'ri import qiling
from .serializers import NoteSerializer, UserSerializer
from .permissions import IsOwner, IsOwnerOrReadOnly  # To'g'ri import qilinganiga ishonch hosil qiling

User = get_user_model()

class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(owner=request.user)
        serializer = NoteSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        # Allow any user to create a new account
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        # All authenticated users can see the list of users
        queryset = self.queryset
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Allow authenticated users to view any user's detail
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Allow users to update their own profile
        user = self.get_object()
        if user != request.user:
            return Response({'detail': 'Not authorized to update this user.'}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Allow users to partially update their own profile
        user = self.get_object()
        if user != request.user:
            return Response({'detail': 'Not authorized to update this user.'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Allow users to delete their own profile
        user = self.get_object()
        if user != request.user:
            return Response({'detail': 'Not authorized to delete this user.'}, status=403)
        return super().destroy(request, *args, **kwargs)
