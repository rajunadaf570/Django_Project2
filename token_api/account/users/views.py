#django/rest_framework imports
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

# app level imports
from .models import (
    User
)

from .serializers import(
    UserRegSerializer,
    UserLoginRequestSerializer,

)
from libs.exceptions import(
    ParseException,
)
from libs.constants import(
    BAD_ACTION,
    BAD_REQUEST,
    )

class UserViewSet(GenericViewSet):

    # @action(methods=['post'], detail=False)
    # def test(self, request):
    #   return Response({'message':'welcome'})

    def get_queryset(self):
        return User.objects.all()

    serializers_dict = {
        # 'login': UserLoginRequestSerializer,
        'register': UserRegSerializer,
        'login':UserLoginRequestSerializer
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False)
    def register(self, request):
        '''
        '''
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = serializer.create(serializer.validated_data)
        if user:
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request):
        '''
        '''
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        print (serializer.validated_data["password"])

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token = user.access_token
        return Response({'token': token},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ])
    def  logout(self, request):

        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)