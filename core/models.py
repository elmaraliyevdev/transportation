from django.db import models
from django.contrib.gis.db import models as gis_models


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    area = gis_models.PolygonField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
