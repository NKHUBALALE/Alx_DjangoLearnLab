from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer  # Create this serializer in notifications/serializers.py

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')