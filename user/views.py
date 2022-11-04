from rest_framework import views, response, exceptions, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from . models import User
from . import serializer as user_serializer
from . import services, authentication
from datetime import datetime

from helper.response_helper import ResponseHelper

from django.utils import timezone


@api_view(['POST'])
# @authentication_classes([authentication.CustomUserAuthentication])
# @permission_classes([permissions.IsAuthenticated])
def add_users(request):
    serializer = user_serializer.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    serializer.instance = services.create_user(user_dc=data)   
    
    response = ResponseHelper.success(serializer.data, "User is added successfully.")    
    return Response(response, 201)


@api_view(['POST'])
def login(request):
    email = request.data["email"]
    password = request.data["password"]

    user = services.user_email_selector(email=email)
    
    if user is None:
        raise exceptions.AuthenticationFailed(ResponseHelper.failed("Invalid credentials."))

    if not user.check_password(raw_password=password):
        raise exceptions.AuthenticationFailed(ResponseHelper.failed("Invalid credentials."))

    user.last_login = timezone.now()
    user.save()

    token = services.create_token(user_id=user.id)

    resp = response.Response()

    resp.set_cookie(key="pmsjwt", value=token, httponly=True, samesite='None', secure='False')
    #resp.set_cookie(key="pmsjwt", value=token, httponly=True)
    resp.data = {"message": "Successfully logged in."}

    return resp


@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user

    serializer = user_serializer.UserSerializer(user)
    
    response = ResponseHelper.success(serializer.data, "User is retrieved successfully.")
    return Response(response)


@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_users(request):
    
    # checking for the parameters from the URL
    users = User.objects.filter(is_active=True)
    serializer = user_serializer.UserSerializer(users, many=True)        
  
    # if there is something in items else raise error
    if users:        
        response = ResponseHelper.success(serializer.data, "Active users are retrieved successfully.")
        return Response(response)
        
    else:

        raise exceptions.NotFoundresponse(ResponseHelper.failed("No active users."))
    
    
@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_archived_users(request):
    
    # checking for the parameters from the URL
    users = User.objects.filter(is_active=False)
    serializer = user_serializer.UserSerializer(users, many=True)        
  
    # if there is something in items else raise error
    if users:        
        response = ResponseHelper.success(serializer.data, "Archived users are retrieved successfully.")
        return Response(response)
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No archived users."))
  


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deactivate_user(request):
    
    data = request.data
        
    email=data["email"]
   
    user = User.objects.get(email=email)
    
    if user.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed("User is already deactivated."))
    
    user.deleted_at = timezone.now()
    user.is_active = False
    
    try:
        user.save()
        response = ResponseHelper.success(email, f"User account with email, {email}, is successfully deactivated.")
        return Response(response, 202)
    
    except:
        raise exceptions.ParseError(ResponseHelper.failed("Invalid argument."))
    

@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def restore_user(request):
    
    data = request.data
        
    email=data["email"]
   
    user = User.objects.get(email=email)
    
    if user.is_active == True:
        raise exceptions.ParseError(ResponseHelper.failed("User is already activated."))
    
    user.deleted_at = None
    user.is_active = True
    
    try:
        user.save()
        response = ResponseHelper.success(email, f"User account with email, {email}, is successfully reactivated.")
        return Response(response, 202)
    
    except:
        raise exceptions.ParseError(ResponseHelper.failed("Invalid argument."))


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    
    resp = response.Response()
    
    token = request.COOKIES.get("pmsjwt")
    
    if(token):
        try:
            resp.delete_cookie(key="pmsjwt", samesite='None')
            resp.data = ResponseHelper.success("Logout", "Successfully logged out.")
            return resp
        except:
            raise exceptions.ParseError(ResponseHelper.failed("Not logged in."))
    else:
        raise exceptions.ParseError(ResponseHelper.failed("Not logged in."))


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def edit_user(request):
    
    data = request.data

    id=data["id"]    
    user = User.objects.get(id=id)   
    
    #update password if given
    if data["password"] or data["confirm_password"]:
        if data["password"] != data["confirm_password"]:            
            raise exceptions.ParseError(ResponseHelper.failed("Passwords do not match."))  
                   
        user.set_password(data["password"])
        user.save()        
    
    user.email = data["email"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.is_staff = data["is_staff"]
    user.is_superuser = data["is_superuser"]
    user.is_active = data["is_active"]
  
    try:
        user.save()
        updated_user = User.objects.get(id=id)
        serializer = user_serializer.UserSerializer(updated_user)
        response = ResponseHelper.success(serializer.data, "User has been updated successfully!")
        return Response(response, 202)
    except:        
        raise exceptions.ParseError(ResponseHelper.failed("Failed to update user."))