from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Project
from .. serializers import ProjectSerializer


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


