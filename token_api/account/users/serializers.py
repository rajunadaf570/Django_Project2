# django imports
from rest_framework import serializers
# from django.contrib.auth import get_user_model  # If used custom user model

# app level imports
from .models import (
    User
)

class UserRegSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)
    first_name = serializers.CharField(required=True, min_length=2)
    last_name = serializers.CharField(required=True, min_length=2)
    mobile = serializers.IntegerField(
        required=False,
        min_value=5000000000,
        max_value=9999999999
    )

    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'first_name', 'last_name', 'mobile')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self,data):
        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginRequestSerializer(serializers.Serializer):
    """
    UserLoginSerializer
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'mobile', 'access_token',
            'is_verified', 'is_active', 'email',
        )

class UserPassUpdateSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model = User
        fields = ('id', 'password')

    def update(self, instance, validated_data):

        if 'password' in validated_data:
             instance.set_password(validated_data.get('password'))
        instance.save()
        return instance