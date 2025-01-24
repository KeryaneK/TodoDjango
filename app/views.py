from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer, TodoSerializer
from .models import Todo


class ServiceStatusAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({'status': 'Service is running'}, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-created_at')

    def delete(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.delete()
        return Response({"message": "TODO item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)