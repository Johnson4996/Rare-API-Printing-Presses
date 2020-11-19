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
from rest_framework.decorators import action
import datetime

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

            try:
                Subscriptions.objects.get()

        for s in subscription:
            s.subscribed = None

            if s.follower_id == request.auth.user.id:
                s.subscribed = True

            else:
                s.subscribed = False

        serializer = SubSerializer(
            subscription, many=True, context={'request': request})
        return Response(serializer.data)

        
    def create(self, request):
        """Handle POST operations
        will be used when user is on uathor profile and hits subscribe
        only info need in the request is the author ID"""

        follower = RareUser.objects.get(user=request.auth.user)
        author = RareUser.objects.get(pk=request.data["author_id"])

        subs = Subscriptions()
        subs.follower = follower
        subs.author = author

        if follower != author:
            try:
                subs.save()
                seralizer = SubSerializer(subs, context={'request': request})
                return Response(seralizer.data)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"reason": "You cannot subscribe to your own posts"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    # Gets only active subscriptions (those without an ended_on) for current user
    def get_currents_subs(self, request):
        subs = Subscriptions.objects.add()
        follower = RareUser.objects.get(user=request.auth.user)

        if follower is not None:
            subs = subs.filter(follower_id=follower, ended_on__isNull=True)

        serializer = SubSerializer(
            subs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    # adds an ended_on for an active subscription between a follower and author
    def unsubscribe(self, request, pk=None):
        sub_obj = Subscriptions.objects.get(pk=pk)

        sub_obj.ended_on = datetime.datetime.now()
        sub_obj.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


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
    follower = SubsUserSeralizer(many=False)

    class Meta:
        model = Subscriptions
        url = serializers.HyperlinkedIdentityField(
            view_name='subscriptions', # this might be wrong
            lookup_field='id')
        fields =('id', 'created_on', 'ended_on', 'follower_id', 'author_id', 'author', 'subscribed')
        depth = 1

    