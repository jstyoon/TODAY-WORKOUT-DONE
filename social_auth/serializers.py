import os
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from . import google
from .register import register_social_user


class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except Exception as exc:
            raise ValidationError('토큰이 유효하지 않거나 만료되었습니다. 다시 로그인해주세요.') from exc

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
