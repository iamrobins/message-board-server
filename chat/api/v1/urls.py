from django.urls import path
from .views import MessageAPIView, AdminAcessAPIView


urlpatterns = [
  path("message/", MessageAPIView.as_view(), name="message"),
  path("admin-access/", AdminAcessAPIView.as_view(), name="admin-access"),
]