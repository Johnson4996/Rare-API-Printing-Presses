from rareapi.models.RareUser import RareUser
from rareapi.models.posts import Posts
from rareapi.models import comments
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comments as CommentsModel

class Comments(ViewSet):
    """Rare Post Comments"""

    def create(self, request):

        author = RareUser.objects.get(user=request.auth.user)

        comment = CommentsModel()

        try:
            comment.content = request.data["content"]
            comment.subject = request.data["subject"]
            comment.created_on = request.data["created_on"]
            post = Posts.objects.get(pk=request.data["postId"])
            comment.post = post
            comment.author = author
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            comment = CommentsModel.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all comments
        Returns:
            Response -- JSON serialized list of comments
        """
        comments = CommentsModel.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = CommentsModel.objects.get(pk=pk)
            comment.delete()
            #if succesful it will return a status code of 204
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except CommentsModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = CommentsModel
        fields = ('id',)

class CommentPostSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = Posts
        fields = ('id', )

class CommentAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = RareUser
        fields = ('id', 'user')


class CommentSerializer(serializers.ModelSerializer):

    post = CommentPostSerializer(many=False)
    author = CommentAuthorSerializer(many=False)

    class Meta:
        model = CommentsModel
        fields = ('id', 'post', 'author', 'content',
                'subject', 'created_on')
        depth = 1