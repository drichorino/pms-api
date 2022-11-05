from django.urls import path
from .views import sites, projects, employees, payslip, daily_time_records

urlpatterns = [
    
    ### SITES ###
    path("sites/add/", sites.add_site, name='add-site'),
    path("sites/list/", sites.list_sites, name='list-sites'), 
    path("sites/archive/", sites.list_archived_sites, name='list-archived-sites'), 
    path("sites/edit/", sites.edit_site, name='edit-site'),    
    path("sites/deactivate/", sites.deactivate_site, name='deactivate-sites'), 
    path("sites/restore/", sites.restore_site, name='restore-site'), 
    path("sites/view/", sites.view_site, name='view-site'),
    
    path("sites/add-project/", sites.add_project_to_site, name='add-project-to-site'),
    
    ### PROJECTS ###
    path("projects/add/", projects.add_project, name='add-project'),
    path("projects/list/", projects.list_projects, name='list-projects'),
    path("projects/archive/", projects.list_archived_projects, name='list-archived-projects'),
    path("projects/edit/", projects.edit_project, name='edit-project'),
    path("projects/deactivate/", projects.deactivate_project, name='deactivate-project'),
    path("projects/restore/", projects.restore_project, name='restore-project'),
    
    ### EMPLOYEES ###
    path("employees/add/", employees.add_employee, name='add-employee'),
    
    
    
]
