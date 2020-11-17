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

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # pk is a parameter to this function, and 
            # Django parses it from the URL rouote parameter
            # http://localhost:8000/posts/2
            #
            # The `2` at the end of the route becomes `pk`

            user = User.objects.get(pk=pk)
            serializer = ProfileUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff')

class ProfileSerializer(serializers.ModelSerializer):

    user = ProfileUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on',
                'active', 'user')
        depth = 1
