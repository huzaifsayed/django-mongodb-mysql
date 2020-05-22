from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Chatbox, ChatboxComponent
from . import serializers
from apps.account.models import User

class ChatboxListView(APIView):

    def get(self, request):
        serializer = serializers.ChatBoxDisplaySerializer(Chatbox.objects.all(), many=True)
        response = {"chatbox": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = serializers.ChatBoxDisplaySerializer(data=data)
        if serializer.is_valid():
            chatbox = Chatbox(**data)
            chatbox.owner_id = 786
            chatbox.save()
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)

class ChatboxDetail(APIView):

    def get_object(self, id):
        try:
            return Chatbox.objects.get(id=id)
        except Chatbox.DoesNotExist:
            raise Http404
        
    def get(self, request, id, format=None):
        chatbox = self.get_object(id)
        serializer = serializers.ChatBoxAddSerializer(chatbox)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        chatbox = self.get_object(id)
        serializer = serializers.ChatBoxAddSerializer(chatbox, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        chatbox = self.get_object(id)
        chatbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChatboxComponentAdd(APIView):

    def get_object(self, id):
        try:
            return Chatbox.objects.get(id=id)
        except Chatbox.DoesNotExist:
            raise Http404
        
    def get(self, request, id, format=None):
        chatbox = self.get_object(id)
        serializer = serializers.ChatBoxAddSerializer(chatbox)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        chatbox = self.get_object(id)
        data = request.data
        print(data)
        serializer = serializers.ChatBoxComponentAddSerializer(data=data)
        if serializer.is_valid():
            chatbox.components.append(ChatboxComponent(**data))
            chatbox.save()
            serializer1 = serializers.ChatBoxAddSerializer(chatbox)
            return Response(serializer1.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatboxComponentUpdate(APIView):

    def get_object(self, id, component_id):
        try:
            return Chatbox.objects(id=id, components__id=component_id)
        except Chatbox.DoesNotExist:
            raise Http404
        
    def delete(self, request, id, component_id, format=None):
        Chatbox.objects(id=id).update_one(
            pull__components__id=component_id
        )
        return Response(status=status.HTTP_204_NO_CONTENT)