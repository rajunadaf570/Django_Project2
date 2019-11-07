#python imports
from random import randint

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
    User,
    UserDetails,
)

from .serializers import(
    UserRegSerializer,
    UserLoginRequestSerializer,
    UserPassUpdateSerializer,
    AddCandidateDetailsSerializer,
    CandidateListSerializer,

)
from libs.exceptions import(
    ParseException,
)
from libs.constants import(
    BAD_ACTION,
    BAD_REQUEST,
    STATUS,
)
from libs import(
    mail,
    redis_client,

)

class UserViewSet(GenericViewSet):

    # def get_queryset(self):
    #     return User.objects.all()

    serializers_dict = {
        'login': UserLoginRequestSerializer,
        'register': UserRegSerializer,
        'resetpassword': UserPassUpdateSerializer
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
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        try: 
             user = serializer.create(serializer.validated_data)
        except Exception as e:
            return Response(({'Failed':str(e)}), status=status.HTTP_409_CONFLICT)
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
    def logout(self, request):

        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def sendotp(self, request):

        email = request.data['email']

        if not User.objects.filter(email=email).exists():
            return Response(BAD_USER, status=status.HTTP_400_BAD_REQUEST)
        """
        save otp in redis
        """
        otp = randint(1000,9999)

        redis_client.store_key_data(email, otp)
        """
        Send otp to mail
        """
        subject = 'G-store otp' 
        message = """Hi,
         {otp} is your G-store password reset code.""".format(otp=otp)
        mail.sendmail.delay(message , subject, [email])
        return Response(({'status':'otp sent to mail'}), status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def resetpassword(self, request):

        try:
            email = request.data['email']
            otp = request.data['otp']

        except Exception as e:
            return Response(({'status':'Failed','detail':str(e.args)}), status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            return Response(BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)
        
        self.objects = User.objects.get(email=email)

        if not redis_client.key_exists(email):
            return Response(BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

        # delete existing value in redis.
        redis_client.remove_key_data(email)

        serializer = self.get_serializer(self.objects, data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        serializer.save()
        return Response(({'status':'password updated successfully'}), status=status.HTTP_200_OK)


class UserDetailViewSet(GenericViewSet):
    '''
    '''
    ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put','delete']
    queryset = UserDetails.objects.all()

    def get_queryset(self,filterdata=None):
        if filterdata:
            self.queryset = UserDetails.objects.filter(**filterdata)
        return self.queryset

    serializers_dict = {
        'addclient': AddCandidateDetailsSerializer,
        'getcandidatelist': CandidateListSerializer,
        'updatecandidatedetail': CandidateListSerializer
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)
    
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ])
    def addclient(self, request):
        """
        """
        data = request.data
        data = data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            print(serializer.errors)
            raise ParseException(BAD_REQUEST, serializer.errors)
        user = serializer.save()
        if user:
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def getcandidatelist(self, request):
        """
        """
        try: 
            data = self.get_serializer(self.get_queryset().filter(user_id=request.user), many=True).data           
            # data = self.get_serializer(self.get_queryset().filter(user_id=request.user,id=request.data['id']), many=True).data
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(({'status':'Failed','result':None,'message':str(e)}),
                status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def updatecandidatedetail(self, request):
        """
        """
        try: 
            data = self.get_serializer(self.get_queryset().filter(
                   user_id=request.user,id=request.data['id']
                ), many=True).data  

            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(({'status':'Failed','result':None,'message':str(e)}),
                status=status.HTTP_404_NOT_FOUND)