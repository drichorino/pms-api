from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Project
from .. serializers import ProjectSerializer

from datetime import datetime


@api_view(['POST'])
def add_project(request):
    serializer = ProjectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    
    project_name = data["name"]
    project = Project(name=project_name)
    
    try:
        project.save()        
    except:
        raise exceptions.ParseError({ "message" : f"Unable to add project, {project_name}."})
    
    return Response({ "message" : f"Project {project_name} is added successfully!"})


@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_projects(request):
    
    # checking for the parameters from the URL
    projects = Project.objects.filter(is_active=True)
    serializer = ProjectSerializer(projects, many=True)        
  
    # if there is something in items else raise error
    if projects:
        
        return Response(serializer.data)
    else:

        raise exceptions.NotFound({"message" : "No active projects."})
    
    
@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_archived_projects(request):
    
    # checking for the parameters from the URL
    projects = Project.objects.filter(is_active=False)
    serializer = ProjectSerializer(projects, many=True)
  
    # if there is something in items else raise error
    if projects:
        
        return Response(serializer.data)
    else:

        raise exceptions.NotFound({"message" : "No archived projects."})
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deactivate_project(request):
    
    data = request.data
        
    project_id = data["id"]
    
    project = Project.objects.get(id=project_id)
    serializer = ProjectSerializer(project)
    project_name = serializer.data["name"]   
     
    to_deactivate = Project.objects.filter(
        is_active=True,
        id=project_id
    ).update(
        is_active=False,
        updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        deleted_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    )
    
    if to_deactivate:     
        
        response = { "message" : f"Project {project_name} has been successfully archived."}
        
        return Response(response, status=202)
    
    else:
        raise exceptions.ParseError({"message" : f"Project {project_name} cannot be found or is already archived."})
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def restore_project(request):
    
    data = request.data
        
    project_id = data["id"]
    
    project = Project.objects.get(id=project_id)
    serializer = ProjectSerializer(project)
    project_name = serializer.data["name"]   
     
    to_activate = Project.objects.filter(
        is_active=False,
        id=project_id
    ).update(
        is_active=True,
        updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        deleted_at = None
    )
    
    if to_activate:     
        
        response = { "message" : f"Project {project_name} has been successfully re-activated."}
        
        return Response(response, status=202)
    
    else:
        raise exceptions.ParseError({"message" : f"Project {project_name} cannot be found or is already activated."})


