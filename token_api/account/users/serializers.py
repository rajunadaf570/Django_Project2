# django imports
from rest_framework import serializers
# from django.contrib.auth import get_user_model  # If used custom user model

# app level imports
from .models import (
    User,
    UserDetails,
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
    UserLoginSerializer.
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

class AddCandidateDetailsSerializer(serializers.ModelSerializer):
    '''
    This class can be used to add the candidate details.
    '''
    mobile = serializers.IntegerField(
        required=True,
        min_value=5000000000,
        max_value=9999999999,
    )
    name = serializers.CharField(required=False, min_length=2)
    email = serializers.EmailField(required=False)
    current_ctc = serializers.IntegerField(required=False)
    expected_ctc = serializers.IntegerField(required=False)
    notice_days = serializers.IntegerField(required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_already_on_notice = serializers.BooleanField(required=False)
    tech_skills  = serializers.JSONField(required=False)
    preferable_locations = serializers.JSONField(required=False)

    class Meta:
        model = UserDetails
        fields = ('id', 'name', 'email', 'current_ctc', 'expected_ctc', 'notice_days', 
         'is_already_on_notice', 'mobile', 'user', 'preferable_locations', 'tech_skills')

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = UserDetails.objects.create(**validated_data)
        user.save()
        return user

class CandidateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetails
        # ordering = ['id']
        fields = ('id', 'name', 'email', 'current_ctc', 'expected_ctc', 'notice_days',
            'is_already_on_notice', 'mobile', 'tech_skills', 'preferable_locations', )

class UpdateCandidateDetailsSerializer(serializers.ModelSerializer):
    """
    Update the details
    """
    mobile = serializers.IntegerField(
        required=True,
        min_value=5000000000,
        max_value=9999999999,
    )
    name = serializers.CharField(required=False, min_length=2)
    email = serializers.EmailField(required=False)
    current_ctc = serializers.IntegerField(required=False)
    expected_ctc = serializers.IntegerField(required=False)
    notice_days = serializers.IntegerField(required=False)
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_already_on_notice = serializers.BooleanField(required=False)
    tech_skills  = serializers.JSONField(required=False)
    preferable_locations = serializers.JSONField(required=False)

    class Meta:
        model = UserDetails
        fields = ('id', 'name', 'email', 'current_ctc', 'expected_ctc', 'notice_days', 
         'is_already_on_notice', 'mobile', 'preferable_locations', 'tech_skills')

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.email = validated_data.get('email')
        instance.current_ctc = validated_data.get('current_ctc')

        instance.expected_ctc = validated_data.get('expected_ctc')
        instance.notice_days = validated_data.get('notice_days')
        instance.is_already_on_notice = validated_data.get('is_already_on_notice')

        instance.mobile = validated_data.get('mobile')
        instance.preferable_locations = validated_data.get('preferable_locations')
        instance.tech_skills = validated_data.get('tech_skills')

        instance.save()
        return instance
