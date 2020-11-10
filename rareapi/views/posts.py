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
        post.image_url = request.data['imageUrl']
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
            # http://localhose:8000/posts/2
            #
            # The `2` at the end of the route becomes `pk`

            post = Posts.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
