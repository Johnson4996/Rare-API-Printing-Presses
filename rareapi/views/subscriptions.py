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

class Subscription(ViewSet):
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