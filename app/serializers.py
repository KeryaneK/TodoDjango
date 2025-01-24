from rest_framework import serializers
from .models import Todo, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']