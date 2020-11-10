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




class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='category',
            lookup_field='id'
        )
        fields = ('id', 'label')
