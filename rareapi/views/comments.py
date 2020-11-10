from rareapi.models import comments
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comments, Posts

class Comments(ViewSet):
    """Rare Post Comments"""

    def create(self, request):

        comment = Comments()

        try:
            comment.content = request.data["content"]
            comment.subject = request.data["subject"]
            comment.created_on = request.data["created_on"]
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = Comments
        fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=False)

    class Meta:
        model = Comments
        fields = ('id', 'title', 'maker', 'gamer',
                'number_of_players', 'skill_level', 'gametype')
        depth = 1