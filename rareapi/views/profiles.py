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

            profiles = RareUser.objects.all().order_by('user')  

            serializer = ProfileSerializer(profiles, many=True, context={'request': request})
            return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #         """Handle GET requests for single profile
    #         Returns:
    #             Response -- JSON serialized profile instance
    #         """
    #         SingleProfile = RareUser.objects.get(pk=pk)
            

    #         try:
    #             RareUser.objects.get(user=request.auth.user, pk=(SingleProfile.id)
    #             SingleProfile.IsAdmin = "Admin"
    #         except RareUser.DoesNotExist:
    #             SingleProfile.IsAdmin = "Author"
    #         try:
    #             serializer = ProfileSerializer(SingleProfile, context={'request': request})
    #             return Response(serializer.data)
    #         except Exception as ex:
    #             return HttpResponseServerError(ex)

class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff')

class ProfileSerializer(serializers.ModelSerializer):

    user = ProfileUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on',
                'active', 'user' )
        depth = 1
