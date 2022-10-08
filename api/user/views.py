from rest_framework import views, response, exceptions, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from . import serializer as user_serializer
from . import services, authentication


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_users(request):
    serializer = user_serializer.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    serializer.instance = services.create_user(user_dc=data)   

    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data["email"]
    password = request.data["password"]

    user = services.user_email_selector(email=email)

    if user is None:
        raise exceptions.AuthenticationFailed({"message" : "Invalid credentials."})

    if not user.check_password(raw_password=password):
        raise exceptions.AuthenticationFailed({"message" : "Invalid credentials."})

    token = services.create_token(user_id=user.id)

    resp = response.Response()

    resp.set_cookie(key="jwt", value=token, httponly=True)
    resp.data = {"message": "Successfully logged in."}

    return resp


@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user

    serializer = user_serializer.UserSerializer(user)

    return response.Response(serializer.data)


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    resp = response.Response()
    resp.delete_cookie("jwt")
    resp.data = {"message": "Successfully logged out."}

    return resp