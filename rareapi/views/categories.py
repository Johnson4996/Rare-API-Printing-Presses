"""View module for handling requests about categories"""
from decimal import Context
from django.db import reset_queries
from rest_framework.status import HTTP_400_BAD_REQUEST
from rareapi.models.categories import Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

class Categories(ViewSet):
    
    def create(self, request):
        """Handle POST request for categories"""

        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle get requests for categories """

        categories = Category.objects.all().order_by('label')
        

        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle Get requests for single category

        Returns:
            Response -- JSON serialized category instance
        """
        try:
            # pk is a parameter to this function, and
            # Django parses it from the URL route parameter
            # http://localhost:8000/categories/2
            #
            # The `2` at the end of the route becomes `pk`

            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({},status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        
        category = Category.objects.get(pk=pk)
        category.label = request.data['label']

        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='categories',
            lookup_field='id'
        )
        fields = ('id', 'url', 'label')
