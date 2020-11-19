"""View module for handling requests about games"""
from rareapi.views.reactions import ReactionSerializer
from rareapi.views.posts import PostUserSerializer
from rareapi.models.RareUser import RareUser
from rareapi.models import PostReactions, Posts, Reaction
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status



class PostReaction(ViewSet):
    """Rare post reactions"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        rareUser = RareUser.objects.get(user=request.auth.user)
        post_reaction = PostReactions()
        post = Posts.objects.get(pk=request.data["post_id"])
        reaction = Reaction.objects.get(pk=request.data["reaction_id"])
        post_reaction.post = post
        post_reaction.reaction = reaction
        post_reaction.rare_user = rareUser

        try:
            post_reaction.save()
            serializer = PostReactionSerializer(post_reaction, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class PostReactionSerializer (serializers.ModelSerializer):

    rare_user = PostUserSerializer(many=False)
    reaction = ReactionSerializer(many=False)

    class Meta:
        model = PostReactions
        fields = ['id', 'rare_user', 'reaction', 'post']
        depth = 1