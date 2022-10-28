from rest_framework import serializers
from .models import Site, Project, Employee, Payslip, DailyTimeRecord



class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ['id']
        
        
class ProjectSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Site
        fields = ['name']   
        read_only_fields = ['id']
        
class EditProjectSerializer(serializers.ModelSerializer):     
    class Meta:
        model = Project
        fields = ['name']   
        read_only_fields = ['id'] 