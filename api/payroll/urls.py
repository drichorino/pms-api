from django.urls import path
from .views import sites, projects, employees, payslip, daily_time_records

urlpatterns = [
    
    ### SITES ###
    path("sites/add/", sites.add_site, name='add-site'),   
    
    ### PROJECTS ###
    path("projects/add/", projects.add_project, name='add-project'),
    path("projects/list/", projects.list_projects, name='list-projects'),
    path("projects/archive/", projects.list_archived_projects, name='list-archived-projects'),
    
    path("projects/deactivate/", projects.deactivate_project, name='deactivate-project'),
    path("projects/restore/", projects.restore_project, name='restore-project'),
    
    ### EMPLOYEES ###
    path("employees/add/", employees.add_employee, name='add-employee'),
    
    
    
]
