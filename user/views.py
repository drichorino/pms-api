from rest_framework import views, response, exceptions, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from . models import User
from . import serializer as user_serializer
from . import services, authentication
from datetime import datetime

from helper.response_helper import ResponseHelper

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
        
    user_email=data["email"]
   
    to_delete = User.objects.filter(
        is_active=True,
        email=user_email
    ).update(
        is_active=False,
        updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        deleted_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    )
    
    if to_delete:     
        
        response = ResponseHelper.success(user_email, f"User account with email, {user_email} is successfully deactivated.")
        return Response(response, 202)
    
    else:
        raise exceptions.ParseError(ResponseHelper.failed("Invalid argument."))
    

@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def restore_user(request):
    
    data = request.data
        
    user_email=data["email"]
   
    to_delete = User.objects.filter(
        is_active=False,
        email=user_email
    ).update(
        is_active=True,
        updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        deleted_at = None
    )
    
    if to_delete:     
        
        response = ResponseHelper.success(user_email, f"User account with email, {user_email} is successfully activated.")
        return Response(response, 202)
    
    else:
        raise exceptions.ParseError(ResponseHelper.failed("Invalid argument."))
    

@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    
    
    resp = response.Response()
    resp.delete_cookie(key="jwt")
    resp.data = {"message": "Successfully logged out."}

    return resp


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def edit_user(request):
    
    data = request.data
    
    id=data["id"]    
   
    if data["password"] or data["confirm_password"]:
        if data["password"] != data["confirm_password"]:
            
            raise exceptions.ParseError(ResponseHelper.failed("Passwords do not match."))    
    
        user = User.objects.filter(id=id).first()        
        user.set_password(data["password"])
        user.save()                     
        
    
    to_update = User.objects.filter(
        id=id
    ).update(
        email = data["email"],
        first_name = data["first_name"],
        last_name = data["last_name"],
        is_staff = data["is_staff"],
        is_superuser = data["is_superuser"],
        is_active = data["is_active"],
        updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    )
        
  
    if to_update:
        
        user = User.objects.filter(id=id).first()
        serializer = user_serializer.UserSerializer(user)

        response = ResponseHelper.success(serializer.data, "User has been updated successfully!")
        return Response(response, 202)
    else:
        
        raise exceptions.ParseError(ResponseHelper.failed("Failed to update user."))