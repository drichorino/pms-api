from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Employee
from .. serializers import EmployeeSerializer

from helper.response_helper import ResponseHelper

from django.utils import timezone


@api_view(['POST'])
def add_employee(request):
    
    data=request.data

