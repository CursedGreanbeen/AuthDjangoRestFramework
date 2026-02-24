import json
import requests

from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import User


def register_new_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data.get('email')).exists():
                return JsonResponse(
                    {'error': 'This email already exists'},
                    status=400
                )

            new_user = User()
            new_user.email = data.get('email')
            new_user.name = data.get('name')
            new_user.surname = data.get('surname')
            new_user.patronymic = data.get('patronymic')
            new_user.cypher_password(data.get('password'))

            new_user.save()

            return JsonResponse(
                {'status': 'ok'},
                status=201
            )

        except:
            pass
