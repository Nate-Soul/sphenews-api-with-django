import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def generate_access_token(user, response):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=15, minutes=0),
        "iat": datetime.utcnow()
    }
    access_token = jwt.encode(
        payload=payload, 
        key=settings.SECRET_KEY, 
        algorithm="HS256"
    )
    set_access_token(response, access_token)


def set_access_token(response, token):
    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
        value=token,
        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    
def set_refresh_token(response, token):
    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
        value=token,
        expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    


   
def delete_tokens_from_cookies(response, token_names):
    for token_name in token_names:
        response.delete_cookie(token_name)

def verify_access_token(request):
    access_token = request.COOKIES.get("access_token")
    
    if access_token:
        try:
            decoded = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            try:
                user = UserModel.objects.only(
                    "username", 
                    "email", 
                    "first_name", 
                    "last_name", 
                    "bio",
                    "role", 
                    "profile_picture",
                    "date_joined",
                    "last_modified"
                ).get(id=decoded["user_id"])
                request.user = user
            except UserModel.DoesNotExist:
                request.user = None
        except jwt.IndexError:
            raise AuthenticationFailed("Expired Token")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid Token")
    else:
        raise AuthenticationFailed("Token not found in cookies")