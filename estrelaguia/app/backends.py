from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, req, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if (user.check_password(password)):
            return user
        return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None
