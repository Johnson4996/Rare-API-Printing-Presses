"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from django.http import request
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Category, Posts, RareUser
from django.contrib.auth.models import User

class Post(ViewSet):
    """Rare Posts"""

    def create(self, request):
        """Handle Post operations

        Returns:
            Response -- JSON serialized post instance
        """

        #Uses the toke passed in the `Authorization` header
        rareUser = RareUser.objects.get(user=request.auth.user)

        # Creat a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.

        post = Posts()
        post.title = request.data['title']
        post.publication_date = request.data['date']
        post.image_url = request.data['image_url']
        post.content = request.data['content']
        post.approved = request.data['approved'] # will need help getting this right
        post.rare_user = rareUser

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `category_id` in the body of the request

        postcategory = Category.objects.get(pk=request.data["category_id"])
        post.category = postcategory

        # Try to save the new post to the database, then
        # serialize the post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            post.save()
            serializer = PostSerializer (post, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    
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

            post = Posts.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Post

        Returns:
            Response -- Empty body with 204 status code
        """

        rareUser = RareUser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of 
        # creating a new instance of Post, get the post record
        # from the database whose primary key is `pk`
        post = Posts()
        post.title = request.data['title']
        post.publication_date = request.data['date']
        post.image_url = request.data['image_url']
        post.content = request.data['content']
        post.approved = request.data['approved'] # will need help getting this right
        post.rare_user = rareUser

        postcategory = Category.objects.get(pk=request.data["category_id"])
        post.category = postcategory
        post.save()

        # 204 status code means everything worked by the
        # server is not sending back any data in the response

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Posts.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Posts.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self, request):
        """Handle Get request to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        # Get all post records from the database
        post = Posts.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = post.filter(user_id=user_id)
        # Support filtering posts by category
        # http://localhost:8000/posts?type=1
        # That URL will retrieve all Music Posts
        # category = self.request.query_params.get('type', None) #type may need to change to category
        # if category is not None:
        #     post = post.filter(category_id=category)

        serializer = PostSerializer(
            post, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class PostUserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""

    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('user', )

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    rare_user = PostUserSerializer(many=False)
    
    class Meta:
        model = Posts
        fields =('id', 'category', 'title', 'rare_user', 'publication_date', 'image_url', 'content', 'approved')
        depth = 1

    