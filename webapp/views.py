from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import User
from .serializer import UserSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=204)


class LoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        if not user_id or not password:
            return Response({'error': 'user_id and password are required'}, status=400)
        user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            designation = user.designation.lower()

            redirect_map = {
                'admin': 'admin-page',
                'director': 'director-page',
                'sending engineer': 'sending-engineer-page',
                'receiving engineer': 'receiving-engineer-page',
                'sending manager': 'sending-manager-page',
                'receiving manager': 'receiving-manager-page'
            }

            redirect_page = redirect_map.get(designation, 'invalid-designation-page')
            return Response({'token': token.key, 'redirect': redirect_page})

        return Response({'error': 'Invalid user_id or password'}, status=401)
