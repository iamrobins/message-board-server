import json
from django.urls import reverse
from rest_framework.test import APITestCase
from chat.models import Message

class MessageAPIViewTestCase(APITestCase):
    def test_messages_get(self):
        url = reverse('message')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_messages_post(self):
        url = reverse('message')
        data = {"content": "Hello"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().content, "Hello")
    
    def test_messages_toxicity_check_post(self):
        url = reverse('message')
        data = {"content": "You're a fool!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(response.status_code, 400)
    
    def test_message_delete_all(self):
        url = reverse("message")
        admin_access_url = reverse("admin-access")
        data = {"content": "Hello"}
        self.client.post(url, data, format='json')
        self.assertEqual(Message.objects.count(), 1)
        admin_access_response = self.client.get(admin_access_url)
        response = self.client.delete(url, {"secret": admin_access_response.data["token"]}, format='json')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(response.status_code, 204)

    def test_message_delete_with_id(self):
        url = reverse("message")
        admin_access_url = reverse("admin-access")
        data = {"content": "Hello"}
        self.client.post(url, data, format='json')
        self.assertEqual(Message.objects.count(), 1)
        message_id = Message.objects.get().id
        admin_access_response = self.client.get(admin_access_url)
        response = self.client.delete(f"{url}?id={message_id}", {"secret": admin_access_response.data["token"]}, format='json')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(response.status_code, 204)



class AdminAccessAPIViewTestCase(APITestCase):
    def test_admin_acces(self):
        url = reverse('admin-access')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)