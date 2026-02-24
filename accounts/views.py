import json
import requests

from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import User


def register_new_user(request):
    if request.method == 'POST':
        try:
            response = requests.get(url, timeout=5)
            data = json.loads(request.body)
            new_user = User()
            new_user.email = data.get('email')
            if User.objects.filter(email=new_user.email).exists():
                new_user.return_json('email', 'This email address already exists!')
            else:
                new_user.name = data.get('name')
                new_user.surname = data.get('surname')
                new_user.patronymic = data.get('patronymic')
                new_user.password = new_user.cypher_password(data.get('password'))
                new_user.save()
            return response.status_code

        except:
            pass
