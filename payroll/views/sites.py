from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Site
from .. serializers import SiteSerializer, EditSiteSerializer

from helper.response_helper import ResponseHelper

from django.utils import timezone


@api_view(['POST'])
def add_site(request):
    
    data=request.data
    site_name = data["name"]
    
    serializer = SiteSerializer(data=data)    
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()     
        response = ResponseHelper.success(site_name, f"Site {site_name} is added successfully!")
        return Response(response, 202)
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
    
    data["name"] = site.name
    data["deleted_at"] = timezone.now()
    data["is_active"] = False

    serializer = SiteSerializer(site, data=data)    
       
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
    
    data["name"] = site.name
    data["deleted_at"] = None
    data["is_active"] = True

    serializer = SiteSerializer(site, data=data)    
       
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
        response = ResponseHelper.success(site.name, "Site has been successfully updated!") 
            
        return Response(response, status=202)
    else:
        raise exceptions.ParseError(ResponseHelper.failed("Failed to update site."))



