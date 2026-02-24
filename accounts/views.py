import json
import requests
import jwt
from datetime import datetime, timedelta

from django.http import JsonResponse
from .models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register_new_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if User.objects.filter(email=data.get('email')).exists():
            return JsonResponse({'error': 'This email already exists'}, status=400)

        new_user = User()
        new_user.email = data.get('email')
        new_user.name = data.get('name')
        new_user.surname = data.get('surname')
        new_user.patronymic = data.get('patronymic')
        new_user.cypher_password(data.get('password'))

        new_user.save()

        return JsonResponse({'status': 'ok'}, status=201)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=401)

        if not user.is_active:
            return JsonResponse({'error': 'Account is disabled'}, status=401)

        if not user.check_password(password):
            return JsonResponse({'error': 'Incorrect password'}, status=401)

        payload = {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=1)}

        try:
            token = jwt.encode(payload, key=settings.SECRET_KEY, algorithm='HS256')
        except Exception as e:
            return JsonResponse(
                {'error': 'Token generation error'},
                status=500
            )

        return JsonResponse({'token': token}, status=200)


@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'logged out'}, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)