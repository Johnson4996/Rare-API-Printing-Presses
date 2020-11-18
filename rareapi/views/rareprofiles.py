from django.core.exceptions import ValidationError
from django.http import request
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import RareUser
from django.contrib.auth.models import User
import uuid
import base64
from django.core.files.base import ContentFile



class RareProfile(ViewSet):
    

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized game instance
        """
        
        try:
            user = RareUser.objects.get(pk=pk)
            serializer = RareProfileSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):
        """Handle Put operations

        Returns:
            Response -- JSON serialized post instance
        """

        rareuser = RareUser.objects.get(user=request.auth.user)

        format, imgstr = request.data['profile_image_url'].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["profile_id"]}-{uuid.uuid4()}.{ext}')
        rareuser.profile_image_url = data

        try:
            rareuser.save()
            serializer = RareProfileSerializer (rareuser, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class RareProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff')

class RareProfileSerializer(serializers.ModelSerializer):

    user = RareProfileUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on',
                'active', 'user')
        depth = 1
