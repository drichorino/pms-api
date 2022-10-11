from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Site
from .. serializers import SiteSerializer


@api_view(['POST'])
def add_site(request):
    serializer = SiteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    
    site_name = data["name"]
    site = Site(name=site_name)
    
    try:
        site.save()        
    except:
        raise exceptions.ParseError({ "message" : f"Unable to add site, {site_name}."})
    
    return Response({ "message" : f"Site {site_name} is added successfully!"})


