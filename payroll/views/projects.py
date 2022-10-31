from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Project
from .. serializers import ProjectSerializer, EditProjectSerializer

from django.utils import timezone

from helper.response_helper import ResponseHelper


@api_view(['POST'])
def add_project(request):
    
    data = request.data
    project_name = data["name"]
    
    serializer = ProjectSerializer(data=data)
    
    if serializer.is_valid(raise_exception=False):
        serializer.save()  
        response = ResponseHelper.success(data, f"Project {project_name} is added successfully!")
        return Response(response, 202)
    else:
        if (serializer.errors["name"]):            
            err = serializer.errors["name"]
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add project, {project_name}. " + err[0]))
        else:            
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add project, {project_name}."))


@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_projects(request):
    
    # checking for the parameters from the URL
    projects = Project.objects.filter(is_active=True)
    serializer = ProjectSerializer(projects, many=True)        
  
    # if there is something in items else raise error
    if projects:        
        return Response(ResponseHelper.success(serializer.data, 'Active projects retrieved successfully!'))
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No active projects."))
    
    
@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_archived_projects(request):
    
    # checking for the parameters from the URL
    projects = Project.objects.filter(is_active=False)
    serializer = ProjectSerializer(projects, many=True)
  
    # if there is something in items else raise error
    if projects:        
        return Response(ResponseHelper.success(serializer.data, 'Archived projects retrieved successfully!'))
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No archived projects."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deactivate_project(request):
    
    data = request.data
        
    id = data["id"]
    
    project = Project.objects.get(id=id)
    
    if project.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed(f"Project {project.name} cannot be found or is already deactivated."))
    
    data["name"] = project.name
    data["deleted_at"] = timezone.now()
    data["is_active"] = False

    serializer = ProjectSerializer(project, data=data)    
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()             
        response = ResponseHelper.success(project.name, f"Project {project.name} has been successfully deactivated.") 
            
        return Response(response, status=202)    
    else:
        raise exceptions.ParseError(ResponseHelper.failed(f"Project {project.name} cannot be found or is already deactivated.")) 
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def restore_project(request):
    
    data = request.data
        
    id = data["id"]
    
    project = Project.objects.get(id=id)
    
    if project.is_active == True:
        raise exceptions.ParseError(ResponseHelper.failed(f"Project {project.name} cannot be found or is already reactivated."))
    
    data["name"] = project.name
    data["deleted_at"] = None
    data["is_active"] = True

    serializer = ProjectSerializer(project, data=data)    
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()             
        response = ResponseHelper.success(project.name, f"Project {project.name} has been successfully reactivated.") 
            
        return Response(response, status=202)    
    else:
        raise exceptions.ParseError(ResponseHelper.failed(f"Project {project.name} cannot be found or is already reactivated."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def edit_project(request):
    
    data = request.data
        
    id = data["id"]
    
    project = Project.objects.get(id=id)
    
    if project.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed(f"Project {project.name} is not active."))

    serializer = EditProjectSerializer(project, data=data)
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()
        response = ResponseHelper.success(project.name, "Project has been updated successfully!")
        return Response(response, 202)
    else:
        if (serializer.errors["name"]):            
            err = serializer.errors["name"]
            raise exceptions.ParseError(ResponseHelper.failed("Unable to update project. " + err[0]))
        else:            
            raise exceptions.ParseError(ResponseHelper.failed("Unable to update project."))

