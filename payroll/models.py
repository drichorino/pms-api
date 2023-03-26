import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Site Name", max_length=100, unique=True)
    projects = ArrayField(
            models.CharField(max_length=100), null=True
        )
    employees = ArrayField(
            models.CharField(max_length=100), null=True
        )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
      return self.name
  
    class Meta:
        db_table = "sites"
        
        
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Project Name', max_length=100, unique=True)
    owner = models.CharField(verbose_name='Project Owner', max_length=100, null=True)
    contract_price = models.DecimalField(verbose_name="Contract Price", max_digits=20, decimal_places=2, null=True)
    total_payment = models.DecimalField(verbose_name="Total Payment", max_digits=20, decimal_places=2, null=True)
    balance = models.DecimalField(verbose_name="Balance", max_digits=20, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
      return self.name
  
    class Meta:
        db_table = "projects"


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name="Employee Name", max_length=100)
    phone_number = models.CharField(verbose_name="Phone Number}", max_length=11, null=True)
    position = models.CharField(verbose_name=" Position", max_length=100, null=True)
    basic_rate = models.DecimalField(verbose_name="Basic Rate", max_digits=20, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)
    site = models.ForeignKey(Site, verbose_name="Site", on_delete=models.CASCADE, null=True)
    projects = ArrayField(
            models.CharField(max_length=100), null=True
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
      return self.name
  
    class Meta:
        db_table = "employees"
        
        
class Payslip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(Employee, verbose_name="DTR's Employee", on_delete=models.CASCADE)
    allowance = models.DecimalField(verbose_name="Allowance", max_digits=20, decimal_places=2, null=True)
    dates = ArrayField(
                models.DateField(),
            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
            
    class Meta:
        db_table = "payslips"
    
    
class DailyTimeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payslip = models.ForeignKey(Payslip, verbose_name="DTR's Payslip", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    time = models.DecimalField(verbose_name="Time", max_digits=3, decimal_places=1)
    projects = ArrayField(
            models.CharField(max_length=100), null=True
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
            
    class Meta:
        db_table = "daily_time_records"
    
    


