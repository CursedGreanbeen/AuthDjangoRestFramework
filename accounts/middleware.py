# accounts/middleware.py
import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import User


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.user = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
            if not user_id:
                return

            user = User.objects.get(id=user_id, is_active=True)
            request.user = user

        except jwt.ExpiredSignatureError:
            return
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return
