from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os

class EmailCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    provider = models.CharField(max_length=50)
    encrypted_token = models.BinaryField()

    def save_token(self, token: str):
        key = os.environ.get('FERNET_KEY').encode()
        f = Fernet(key)
        self.encrypted_token = f.encrypt(token.encode())

    def get_token(self):
        key = os.environ.get('FERNET_KEY').encode()
        f = Fernet(key)
        return f.decrypt(self.encrypted_token).decode()