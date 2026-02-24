import bcrypt
from django.db import models


ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('user', 'User'),
        ('guest', 'Guest'),
    ]


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)  # check length
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    role = models.CharField(choices=ROLE_CHOICES, default='guest')
    is_active = models.BooleanField(default=True)

    def cypher_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            salt
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
