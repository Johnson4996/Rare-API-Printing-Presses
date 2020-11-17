"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from django.http import request
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import RareUser, Subscriptions
from django.contrib.auth.models import User
from rareapi.views.posts import UserSerializer

class Subs(ViewSet):
    """Rare Subscriptions"""

    def list(self, request):
        """Handle Get request to subscriptions resource

        Returns:
            Response -- JSON serialized list of subscriptions
        """
        # Get all subscription records from the database
        subscription = Subscriptions.objects.all()

        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            subscription = subscription.filter(user_id=user_id)

        serializer = SubSerializer(
            subscription, many=True, context={'request': request})
        return Response(serializer.data)

class SubsUserSeralizer(serializers.ModelSerializer):
    """JSON serializer for subscriptions"""

    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('user', )

class SubSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for subscriptions

    Arguments:
        serializer type
    """
    
    author = SubsUserSeralizer(many=False)

    class Meta:
        model = Subscriptions
        fields =('id', 'created_on', 'ended_on', 'follower_id', 'author_id', 'author')
        depth = 1