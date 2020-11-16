"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import RareUser
from django.contrib.auth.models import User


class CurrentUser(ViewSet):
    """Rare tags"""

    def retrieve(self, request, pk = None):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        user = RareUser.objects.get(user=request.auth.user)
        # Get all game records from the database

        serializer = RareUserSerializer(
            user, many=False, context={'request': request})
        return Response(serializer.data)

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializer type
    """
    class Meta:
        model = RareUser
        fields = ('id',)
