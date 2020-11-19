"""View for handling post reactions"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Reaction



class Reactions(ViewSet):
   

    def create(self, request):
        """Handle POST request for categories"""

        reaction = Reaction()
        reaction.label = request.data["label"]
        reaction.image_url = request.data["image_url"]

        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()

            return Response({},status=status.HTTP_204_NO_CONTENT)

        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle get requests for categories """

        reactions = Reaction.objects.all().order_by('label')
        

        serializer = ReactionSerializer(reactions, many=True, context={'request': request})
        return Response(serializer.data)


class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for reactions"""

    class Meta:
        model = Reaction
        url = serializers.HyperlinkedIdentityField(
            view_name='reactions',
            lookup_field='id'
        )
        fields = ('id', 'label', 'image_url')
