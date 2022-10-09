from rest_framework import serializers
from models import Site, Project, Employee, Payslip, DailyTimeRecord



class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
        
class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = '__all__'
        

class DailyTimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTimeRecord
        fields = '__all__'      
