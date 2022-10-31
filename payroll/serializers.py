from rest_framework import serializers
from .models import Site, Project, Employee, Payslip, DailyTimeRecord
from rest_framework.validators import UniqueValidator




class SiteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Site.objects.all(), message="Site already exists!")]
    )
    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ['id']
        
     
        
class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Project.objects.all(), message="Project already exists!")]
    )
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id']
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id']
        
        
class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = '__all__'
        read_only_fields = ['id']
        

class DailyTimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTimeRecord
        fields = '__all__'
        read_only_fields = ['id']    
        
        
        
##### EDIT SERIALIZERS #####       
        
class EditSiteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Site.objects.all(), message="Site name already exists!")]
    )
    class Meta:
        model = Site
        fields = ['name']   
        read_only_fields = ['id']
        
class EditProjectSerializer(serializers.ModelSerializer):     
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Project.objects.all(), message="Project name already exists!")]
    )
    class Meta:
        model = Project
        fields = ['name']   
        read_only_fields = ['id'] 