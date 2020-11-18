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

    @action(methods=['get', 'post', 'delete'], detail=True)
    def follow(self, request, pk=None):
        """Managing followers subscribing to authors"""

        # A user wants to subscribe to an author
        if request.method == "POST":
            subs = Subscriptions.object.get(pk=pk)

        # Django uses the `Authorization` header to determine
        # which user is making the request to subscribe

            author = RareUser.objects.get(user=request.auth.user)

            try:
        #Determine if the user is already following
                subscribe = Subscriptions.objects.get(
                    follower_id=user_id) #will need help with this
                return Response(
                    {'message': 'You are already subscribed to this Author'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            except Subscriptions.DoesNotExist:
            # The user is not signed up
                subscribe = Subscriptions()
                subscribe.subs = subs
                subscribe.author = author
                subscribe.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # User wants to Unsubscribe
        elif request.method == "DELETE":
            # handle the case if the client wants to 
            # unfollow
            try:
                subs = Subscriptions.objects.get(pk=pk)
            except Subscriptions.DoesNotExist:
                return Response(
                    {'message': 'You do not follow this author'},
                    status=status.HTTP_400_BAD_REQUEST)

        # Get the authenticated user
            follower = RareUser.objects.get(user=request.auth.user)

            try:
                # try to unsubscribe
                subs = Subscriptions.objects.get(
                    follower_id=user_id) # will need help with this
                subs.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except Subscriptions.DoesNotExist:
                return Response(
                    {'message': 'Not currently subscribed to author'},
                    status=status.HTTP_404_NOT_FOUND)

    # If the client performs a request with a method that isnt
    # POST or DELETE, tell the client the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

    