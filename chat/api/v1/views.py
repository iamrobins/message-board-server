import traceback
import logging
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from chat.models import Message
from chat.serializers import MessageSerializer
from chat import utils
from chat.permissions import JWTAuthentication

class MessageAPIView(APIView):
  def get(self, request):
    try:
      messages = Message.objects.all().order_by('-created_at')[:10]
      # messages = Message.objects.all()
      serializer = MessageSerializer(messages, many=True)
    except Exception as e:
      logging.error(traceback.format_exc())
      return Response(str(e), 400)

    return Response(serializer.data, 200)

  def post(self, request):
    try:
      ip_addr = utils.get_ip_address(request)
      if not ip_addr: return Response("Unable to get the ip_address", 400)

      is_toxic = utils.check_toxicity(request.data["content"])
      if is_toxic: return Response("Toxicity Not Allowed", 400)

      request.data["source"] = ip_addr
      serializer = MessageSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
    except Exception as e:
      logging.error(traceback.format_exc())
      return Response({ "error": str(e) }, 400)
    
    return Response(serializer.data, 201)

  def delete(self, request):
    try:
      payload = JWTAuthentication.authenticate(request)
      if payload["scope"] != "admin": raise Exception("Only admins are allowed to perform this action")
      
      id = request.query_params.get("id")

      if not id:
        messages = Message.objects.all().delete()
        return Response({"success": "All messages successfully deleted"}, 204)
      else:
        message = Message.objects.filter(id=id)
        if not message:
          raise Exception("Message not found")
        message.delete()
        return Response({"success": "Message successfully deleted"}, 204)
      
    except Exception as e:
      logging.error(traceback.format_exc())
      return Response({ "error": str(e) }, 400)

class AdminAcessAPIView(APIView):
  def get(self, request):
    try:
      token = JWTAuthentication.generate_jwt(scope="admin")
      response = Response()

      response.set_cookie("secret", token, httponly=True)
      response.data = {"token": token}

      return response
    except Exception as e:
      logging.error(traceback.format_exc())
      return Response({ "error": str(e) }, 400)