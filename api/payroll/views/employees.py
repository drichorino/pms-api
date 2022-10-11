from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Employee
from .. serializers import EmployeeSerializer


@api_view(['POST'])
def add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    
    empolyee_name = data["name"]
    site = Employee(
            name=empolyee_name,
            position=data["position"],
            site=data["site"],
            basic_rate=data["basic_rate"]
            )
    
    try:
        site.save()        
    except:
        raise exceptions.ParseError({ "message" : f"Unable to add employee, {empolyee_name}."})
    
    return Response({ "message" : f"Employee {empolyee_name} is added successfully!"})


