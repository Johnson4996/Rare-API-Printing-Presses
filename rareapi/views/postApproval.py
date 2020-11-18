from django.core.exceptions import ValidationError
from django.http import request
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Posts, RareUser
from django.contrib.auth.models import User


class ApprovePost(ViewSet):
    
    def update(self, request, pk=None):
        """Handle PUT requests for a Post

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of 
        # creating a new instance of Post, get the post record
        # from the database whose primary key is `pk`
        post = Posts.objects.get(pk=pk)

        if post.approved == True:
            post.approved = False
        else: 
            post.approved = True
        post.save()

        # 204 status code means everything worked by the
        # server is not sending back any data in the response

        return Response({}, status=status.HTTP_204_NO_CONTENT)

# class ProfileUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'is_staff')

# class ProfileSerializer(serializers.ModelSerializer):

#     user = ProfileUserSerializer(many=False)

#     class Meta:
#         model = RareUser
#         fields = ('id', 'bio', 'profile_image_url', 'created_on',
#                 'active', 'user')
#         depth = 1
