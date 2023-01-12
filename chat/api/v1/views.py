from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from chat.models import Message
from chat.serializers import MessageSerializer
from chat import utils


class MessageAPIView(APIView):

  def get(self, request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data, 200)

  def post(self, request):
    ip_addr = utils.get_ip_address(request)
    if not ip_addr:
      return Response("Unable to get the ip_address", 400)

    request.data["source"] = ip_addr
    
    serializer = MessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response(serializer.data, 201)