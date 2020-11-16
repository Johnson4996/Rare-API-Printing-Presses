from django.core.exceptions import ValidationError
from django.http import request
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import RareUser
from django.contrib.auth.models import User


class Profile(ViewSet):
    
    def list(self, request):
            """Handle get requests for profiles """

            profiles = RareUser.objects.all()
            

            serializer = ProfileSerializer(profiles, many=True, context={'request': request})
            return Response(serializer.data)

class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')

class ProfileSerializer(serializers.ModelSerializer):

    user = ProfileUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on',
                'active', 'user' )
        depth = 1
