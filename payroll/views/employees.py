from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Employee
from .. serializers import EmployeeSerializer, EditEmployeeSerializer

from helper.response_helper import ResponseHelper

from django.utils import timezone


@api_view(['POST'])
def add_employee(request):    
    
    data=request.data
    employee_name = data["name"]
    
    serializer = EmployeeSerializer(data=data)    
    
    if serializer.is_valid(raise_exception=False):
        serializer.save()     
        response = ResponseHelper.success(employee_name, f"Employee {employee_name} is added successfully!")
        return Response(response, 202)
    else:        
        if (serializer.errors):
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add employee, {employee_name}."))
        else:            
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add employee, {employee_name}."))


@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_employees(request):

    employees = Employee.objects.filter(is_active=True)
    serializer = EmployeeSerializer(employees, many=True)        
  
    if employees:        
        return Response(ResponseHelper.success(serializer.data, 'Active employees retrieved successfully!'))
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No active employees."))
    
    
@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_archived_employees(request):

    employees = Employee.objects.filter(is_active=False)
    serializer = EmployeeSerializer(employees, many=True)        
  
    if employees:        
        return Response(ResponseHelper.success(serializer.data, 'Archived employees retrieved successfully!'))
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No archived employees."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deactivate_employee(request):
    
    data = request.data
        
    id = data["id"]
    
    employee = Employee.objects.get(id=id)
    
    if employee.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed(f"Employee {employee.name} cannot be found or is already deactivated."))
    
    serializer = EmployeeSerializer(employee)
    serializedEmployee = serializer.data
    
    serializedEmployee["deleted_at"] = timezone.now()
    serializedEmployee["is_active"] = False

    serializer = EmployeeSerializer(employee, data=serializedEmployee)    
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()             
        response = ResponseHelper.success(employee.name, f"Employee {employee.name} has been successfully deactivated.") 
            
        return Response(response, status=202)    
    else:
        raise exceptions.ParseError(ResponseHelper.failed(f"Employee {employee.name} cannot be found or is already deactivated."))  
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def restore_employee(request):
    
    data = request.data
        
    id = data["id"]
    
    employee = Employee.objects.get(id=id)
    
    if employee.is_active == True:
        raise exceptions.ParseError(ResponseHelper.failed(f"Employee {employee.name} cannot be found or is already activated."))
    
    serializer = EmployeeSerializer(employee)
    serializedEmployee = serializer.data
    
    serializedEmployee["deleted_at"] = None
    serializedEmployee["is_active"] = True

    serializer = EmployeeSerializer(employee, data=serializedEmployee)     
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()             
        response = ResponseHelper.success(employee.name, f"Employee {employee.name} has been successfully reactivated.") 
            
        return Response(response, status=202)    
    else:
        raise exceptions.ParseError(ResponseHelper.failed(f"Employee {employee.name} cannot be found or is already activated."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def edit_employee(request):
    
    data = request.data
        
    id = data["id"]
    employee_name = data["name"]
    
    employee = Employee.objects.get(id=id)
    
    if employee.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed(f"Employee {employee.name} is not active."))

    serializer = EditEmployeeSerializer(employee, data=data)    
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()
        response = ResponseHelper.success(serializer.data, "Employee has been updated successfully!")
        return Response(response, 202)
    else:
        if (serializer.errors):
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to update employee, {employee_name}."))
        else:            
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to update employee., {employee_name}"))