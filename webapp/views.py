from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializer

class UserList(APIView):
    def get(self, request):
        items = User.objects.all()
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFindById(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        data = self.get_object(pk)
        if data is None:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
