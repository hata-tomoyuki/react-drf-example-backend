from django.contrib.auth import login
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserLoginSerializer, UserRegisterSerializer
from rest_framework.authtoken.models import Token



class UserRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserLoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = Token.objects.get_or_create(user=serializer.validated_data)
            return Response({'token': token[0].key}, status=200)
        return Response(serializer.errors, status=400)
