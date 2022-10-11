from django.urls import path
from .views import sites, projects, employees, payslip, daily_time_records

urlpatterns = [
    
    ### SITES ###
    path("add-site/", sites.add_site, name='add-site'),   
    
    ### PROJECTS ###
    path("add-project/", projects.add_project, name='add-project'),
    
    ### EMPLOYEES ###
    path("add-employee/", employees.add_employee, name='add-employee'),
    
    
    
]
