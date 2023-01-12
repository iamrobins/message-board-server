import jwt
import datetime
from rest_framework import exceptions
from message_board.settings import SECRET_KEY

class JWTAuthentication():

  @staticmethod
  def authenticate(request):
      token = request.data["secret"]

      if not token:
        return None

      try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
      except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("unauthenticated")

      return payload

  @staticmethod
  def generate_jwt(scope: str):
    payload = {
      "scope": scope,
      "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
      "iat": datetime.datetime.utcnow()
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")