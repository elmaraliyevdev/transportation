from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from django.contrib.gis import geos
from rest_framework import status


@api_view(['GET'])
def get_service_areas_by_point(request):
    """
    API endpoint that allows to list service areas that include the given lat/lng
    """
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)

    if latitude and longitude:
        point = geos.Point(float(longitude), float(latitude))
        queryset = ServiceArea.objects.filter(area__contains=point)
        serializer = ServiceAreaSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        queryset = ServiceArea.objects.all()
        serializer = ServiceAreaSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_service_area(request, pk):
    try:
        service_area = ServiceArea.objects.get(pk=pk)
    except ServiceArea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single service area
    if request.method == 'GET':
        serializer = ServiceAreaSerializer(service_area)
        return Response(serializer.data)
    # delete a single service area
    elif request.method == 'DELETE':
        service_area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single service area
    elif request.method == 'PUT':
        serializer = ServiceAreaSerializer(service_area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_provider(request, pk):
    try:
        provider = Provider.objects.get(pk=pk)
    except Provider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single provider
    if request.method == 'GET':
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)
    # update details of a single provider
    elif request.method == 'PUT':
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete a single provider
    elif request.method == 'DELETE':
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def get_post_providers(request):
    # get all providers
    if request.method == 'GET':
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

    # insert a new record for a provider
    if request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'phone_number': request.data.get('phone_number'),
            'language': request.data.get('language'),
            'currency': request.data.get('currency'),
        }
        serializer = ProviderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_service_areas(request):
    # get all service areas
    if request.method == 'GET':
        service_areas = ServiceArea.objects.all()
        serializer = ServiceAreaSerializer(service_areas, many=True)
        return Response(serializer.data)
    # insert a new record for a service area
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'area': request.data.get('area'),
            'provider': request.data.get('provider'),
        }
        serializer = ServiceAreaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
