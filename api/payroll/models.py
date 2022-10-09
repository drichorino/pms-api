import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Site Name", max_length=100, unique=True)

    def __str__(self):
      return self.name
  
    class Meta:
        db_table = "sites"
        
        
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Project Name', max_length=100, unique=True)

    def __str__(self):
      return self.name
  
    class Meta:
        db_table = "projects"


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    site = models.ForeignKey(Site, verbose_name="Employee's Site", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Employee Name", max_length=100)
    position = models.CharField(verbose_name="Employee's Postion", max_length=100)
    basic_rate = models.DecimalField(verbose_name="Employee's Basic Rate", max_digits=20, decimal_places=2)

    def __str__(self):
      return self.name
  
    class Meta:
        db_table = "employees"
        
        
class Payslip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(Employee, verbose_name="DTR's Employee", on_delete=models.CASCADE)
    dates = ArrayField(
                models.DateField(),
            )
            
    class Meta:
        db_table = "payslips"
    
    
class DailyTimeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payslip = models.ForeignKey(Payslip, verbose_name="DTR's Payslip", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="DTR's Date")
    time = models.DecimalField(verbose_name="DTR's Time", max_digits=3, decimal_places=1)
    projects = ArrayField(
                    models.IntegerField(verbose_name="DTR's Projects'")
                )
            
    class Meta:
        db_table = "daily_time_records"
    
    


