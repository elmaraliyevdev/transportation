from rest_framework.response import Response
from rest_framework import viewsets
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from django.contrib.gis import geos


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows service areas to be viewed or edited.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    def list(self, request, *args, **kwargs):

        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        if latitude and longitude:
            point = geos.Point(float(longitude), float(latitude))
            queryset = ServiceArea.objects.filter(area__contains=point)
            serializer = ServiceAreaSerializer(queryset, many=True)

            return Response(serializer.data)

        else:
            queryset = ServiceArea.objects.all()
            serializer = ServiceAreaSerializer(queryset, many=True)

            return Response(serializer.data)
