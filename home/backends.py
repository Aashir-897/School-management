from django.contrib.auth.backends import BaseBackend
from .models import Student

class StudentBackend(BaseBackend):
    def authenticate(self, request, roll_number=None, name=None, **kwargs):
        try:
            # Try to get the student with the provided roll number and name
            return Student.objects.get(roll_number=roll_number, name=name)
        except Student.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
