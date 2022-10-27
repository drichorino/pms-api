from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import exceptions, permissions
from user import authentication

from .. models import Site
from .. serializers import SiteSerializer

from helper.response_helper import ResponseHelper


@api_view(['POST'])
def add_site(request):
    serializer = SiteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    
    site_name = data["name"]
    site = Site(name=site_name)
    
    try:
        site.save()     
        response = ResponseHelper.success(site_name, f"Site {site_name} is added successfully!")   
        return Response(response, 202)
    except:
        raise exceptions.ParseError(ResponseHelper.failed(f"Unable to add site, {site_name}."))


