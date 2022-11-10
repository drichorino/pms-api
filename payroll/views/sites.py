from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Site, Project
from .. serializers import SiteSerializer, EditSiteSerializer, ViewSiteSerializer, GetProjectsNotInSiteSerializer, ProjectSerializer

from helper.response_helper import ResponseHelper

from django.utils import timezone


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_site(request):
    
    data=request.data
    site_name = data["name"]
    
    serializer = SiteSerializer(data=data)    
    
    if serializer.is_valid(raise_exception=False):
        serializer.save()     
        response = ResponseHelper.success(site_name, f"Site {site_name} is added successfully!")
        return Response(response, 202)
    else:
        if (serializer.errors["name"]):            
            err = serializer.errors["name"]
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add site, {site_name}. " + err[0]))
        else:            
            raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add site, {site_name}."))
    
    
@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_sites(request):

    sites = Site.objects.filter(is_active=True)
    serializer = SiteSerializer(sites, many=True)        
  
    if sites:        
        return Response(ResponseHelper.success(serializer.data, 'Active sites retrieved successfully!'))
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No active sites."))
    
    
@api_view(['GET'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_archived_sites(request):
    
    sites = Site.objects.filter(is_active=False)
    serializer = SiteSerializer(sites, many=True)        
  
    if sites:        
        return Response(ResponseHelper.success(serializer.data, 'Archived sites retrieved successfully!'))
    else:
        raise exceptions.NotFound(ResponseHelper.failed("No Archived sites."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deactivate_site(request):
    
    data = request.data
        
    id = data["id"]
    
    site = Site.objects.get(id=id)
    
    if site.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed(f"Site {site.name} cannot be found or is already deactivated."))
    
    serializer = SiteSerializer(site)
    serializedSite = serializer.data
    
    serializedSite["deleted_at"] = timezone.now()
    serializedSite["is_active"] = False

    serializer = SiteSerializer(site, data=serializedSite)
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()             
        response = ResponseHelper.success(site.name, f"Site {site.name} has been successfully deactivated.") 
            
        return Response(response, status=202)    
    else:
        raise exceptions.ParseError(ResponseHelper.failed(f"Site {site.name} cannot be found or is already deactivated."))  
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def restore_site(request):
    
    data = request.data
        
    id = data["id"]
    
    site = Site.objects.get(id=id)
    
    if site.is_active == True:
        raise exceptions.ParseError(ResponseHelper.failed(f"Site {site.name} cannot be found or is already activated."))
    
    serializer = SiteSerializer(site)
    serializedSite = serializer.data
    
    serializedSite["deleted_at"] = None
    serializedSite["is_active"] = True

    serializer = SiteSerializer(site, data=serializedSite)  
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()             
        response = ResponseHelper.success(site.name, f"Site {site.name} has been successfully reactivated.") 
            
        return Response(response, status=202)    
    else:
        raise exceptions.ParseError(ResponseHelper.failed(f"Site {site.name} cannot be found or is already activated."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def edit_site(request):
    
    data = request.data
        
    id = data["id"]
    
    site = Site.objects.get(id=id)
    
    if site.is_active == False:
        raise exceptions.ParseError(ResponseHelper.failed(f"Site {site.name} is not active."))

    serializer = EditSiteSerializer(site, data=data)    
       
    if serializer.is_valid(raise_exception=False):
        serializer.save()
        response = ResponseHelper.success(site.name, "Site has been updated successfully!")
        return Response(response, 202)
    else:
        if (serializer.errors["name"]):            
            err = serializer.errors["name"]
            raise exceptions.ParseError(ResponseHelper.failed("Unable to update site. " + err[0]))
        else:            
            raise exceptions.ParseError(ResponseHelper.failed("Unable to update site."))


@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def view_site(request):
    
    data = request.data
    
    id = data["id"]   
    
    site = Site.objects.filter(id=id).first()   
    
    if site:   
        siteSerializer = ViewSiteSerializer(site)
        siteData = siteSerializer.data       
        
        
        #GET PROJECTS NOT IN SITE
        if(siteData['projects']):        
            projectsNotInSite = Project.objects.exclude(id__in=siteData['projects'])
        else:
            projectsNotInSite = Project.objects.all()
        
        projectsNotInSiteSerializer = GetProjectsNotInSiteSerializer(projectsNotInSite, many=True)
        projectsNotInSiteData = projectsNotInSiteSerializer.data
        
        
        #GET PROJECTS IN SITES
        if(siteData['projects']):        
            projectsInSite = Project.objects.filter(id__in=siteData['projects'])
        else:
            projectsInSite =[]
        
        projectsInSiteSerializer = ProjectSerializer(projectsInSite, many=True)
        projectsInSiteData = projectsInSiteSerializer.data
        
                    
        responseObject = { "site" : siteData, "projects_not_in_site" : projectsNotInSiteData, "projects_in_site" : projectsInSiteData }
        
        response = ResponseHelper.success(responseObject, "Site has been retrieved successfully!")
        return Response(response)
    else:            
        raise exceptions.ParseError(ResponseHelper.failed("Site not found."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_project_to_site(request):
    
    data = request.data
    
    id = data['id']
    projects_to_add = data['projects_to_add']
    
    site = Site.objects.filter(id=id).first()
    
    if site.projects:
        (site.projects).extend(projects_to_add)
    else:    
        site.projects = projects_to_add
    
    try: 
        site.save()
        response = ResponseHelper.success(id, f"Project(s) has been added to {site}.")
        return Response(response)
    except:
        raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add project(s) to {site}."))
    
    
@api_view(['POST'])
@authentication_classes([authentication.CustomUserAuthentication])
@permission_classes([permissions.IsAuthenticated])
def unassign_project(request):
    
    data = request.data
    
    site_id = data['site_id']
    project_id = data['project_id']
       
    site = Site.objects.filter(id=site_id).first()    

    try: 
        (site.projects).remove(project_id)
        site.save()
        response = ResponseHelper.success(project_id, f"Project(s) has been unassigned from {site}.")
        return Response(response)
    except:
        raise exceptions.ParseError(ResponseHelper.failed(f"Unable to unassign project(s) from {site}."))