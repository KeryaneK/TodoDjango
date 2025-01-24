from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    RegisterAPIView,
    ServiceStatusAPIView,
    TodoListCreateAPIView,
    TodoRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path('service_status', ServiceStatusAPIView.as_view(), name='service_status'),
    path('auth/register', RegisterAPIView.as_view(), name='register'),
    path('auth/token', obtain_auth_token, name='token'),
    path('todos', TodoListCreateAPIView.as_view(), name='todo_list'),
    path('todos/<int:pk>', TodoRetrieveUpdateDestroyAPIView.as_view(), name='todo_detail')
]