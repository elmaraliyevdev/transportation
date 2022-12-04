from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.gis import geos

from core.serializers import ProviderSerializer, ServiceAreaSerializer
from core.models import Provider, ServiceArea

client = Client()


class GetAllProvidersTest(TestCase):
    """ Test module for GET all providers API """

    def setUp(self):
        Provider.objects.create(
            name="Fedex",
            email="fedex@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD",
        )
        Provider.objects.create(
            name="DHL",
            email="dhl@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD",
        )
        Provider.objects.create(
            name="UPS",
            email="ups@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD",
        )

    def test_get_all_providers(self):
        # get API response
        response = client.get(reverse("get_post_providers"))
        # get data from db
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProviderTest(TestCase):
    """ Test module for GET single provider API """

    def setUp(self):
        self.ups = Provider.objects.create(
            name="UPS",
            email="ups@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD",
        )

        self.fedex = Provider.objects.create(
            name="FedEx",
            email="fedex@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD",
        )

        self.dhl = Provider.objects.create(
            name="DHL",
            email="dhl@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD",
        )

    def test_get_valid_single_provider(self):
        response = client.get(
            reverse("get_delete_update_provider", kwargs={"pk": self.ups.pk})
        )
        provider = Provider.objects.get(pk=self.ups.pk)
        self.assertEqual(response.data["name"], provider.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_provider(self):
        response = client.get(
            reverse("get_delete_update_provider", kwargs={"pk": 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewProviderTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "name": "Test Provider",
            "email": "test@gmail.com",
            "phone_number": "1234567890",
            "language": "English",
            "currency": "USD"
        }

        self.invalid_payload = {
            "name": "",
            "email": "test@gmail.com",
            "phone_number": "1234567890",
            "language": "English",
            "currency": "USD",
        }

    def test_create_valid_provider(self):
        response = client.post(
            reverse('get_post_providers'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_provider(self):
        response = client.post(
            reverse('get_post_providers'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateProviderTest(TestCase):
    def setUp(self):
        self.ups = Provider.objects.create(
            name="UPS",
            email="test@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD"
        )

        self.fedex = Provider.objects.create(
            name="Fedex",
            email="fedex@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD"
        )

        self.valid_payload = {
            "name": "Fedex",
            "email": "fedex@gmail.com",
            "phone_number": "1234567890",
            "language": "English",
            "currency": "USD"
        }

        self.invalid_payload = {
            "name": "",
            "email": "ups@gmail.com",
            "phone_number": "1234567890",
            "language": "English",
            "currency": "USD",
        }

    def test_update_valid_provider(self):
        response = client.put(
            reverse('get_delete_update_provider', kwargs={'pk': self.ups.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_provider(self):
        response = client.put(
            reverse('get_delete_update_provider', kwargs={'pk': self.fedex.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteProviderTest(TestCase):
    """ Test module for deleting an existing provider record """

    def setUp(self):
        self.ups = Provider.objects.create(
            name="UPS",
            email="ups@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD"
        )

        self.fedex = Provider.objects.create(
            name="Fedex",
            email="fedex@gmail.com",
            phone_number="1234567890",
            language="English",
            currency="USD"
        )

    def test_valid_delete_provider(self):
        response = client.delete(
            reverse('get_delete_update_provider', kwargs={'pk': self.ups.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_provider(self):
        response = client.delete(
            reverse('get_delete_update_provider', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllServiceAreasTest(TestCase):
    """ Test module for GET all service areas API """

    def setUp(self):
        ServiceArea.objects.create(
            name="Service Area 1",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="UPS",
                email="ups@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

        ServiceArea.objects.create(
            name="Service Area 2",
            price=20,
            area="POLYGON((35 10, 45 45, 15 40, 10 20, 35 10))",
            provider=Provider.objects.create(
                name="Fedex",
                email="fedex@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

        self.latitude = 37.7749
        self.longitude = -122.4194

    def test_get_all_service_areas(self):
        # get API response
        response = client.get(reverse('get_post_service_areas'))
        # get data from db
        service_areas = ServiceArea.objects.all()
        serializer = ServiceAreaSerializer(service_areas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_service_areas_by_point(self):
        # get API response
        response = client.get('/api/get-service-areas-by-point/', {'latitude': self.latitude, 'longitude': self.longitude})
        # get data from db
        service_areas = ServiceArea.objects.filter(area__contains=geos.Point(self.latitude, self.longitude))
        serializer = ServiceAreaSerializer(service_areas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleServiceAreaTest(TestCase):
    """ Test module for GET single service area API """

    def setUp(self):
        self.service_area_1 = ServiceArea.objects.create(
            name="Service Area 1",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="UPS",
                email="ups@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

        self.service_area_2 = ServiceArea.objects.create(
            name="Service Area 2",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="DHL",
                email="dhl@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

    def test_get_valid_single_service_area(self):
        response = client.get(
            reverse('get_delete_update_service_area', kwargs={'pk': self.service_area_1.pk}))
        service_area = ServiceArea.objects.get(pk=self.service_area_1.pk)
        serializer = ServiceAreaSerializer(service_area)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_service_area(self):
        response = client.get(
            reverse('get_delete_update_service_area', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewServiceAreaTest(TestCase):
    """ Test module for inserting a new service area """

    def setUp(self):
        self.valid_payload = {
            "name": "Service Area 1",
            "price": 10,
            "area": "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            "provider": Provider.objects.create(
                name="UPS",
                email="ups@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            ).pk
        }

        self.invalid_payload = {
            "name": "Service Area 1",
            "price": 10,
            "area": "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            "provider": 30,
        }

    def test_create_valid_service_area(self):
        response = client.post(
            reverse('get_post_service_areas'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_service_area(self):
        response = client.post(
            reverse('get_post_service_areas'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleServiceAreaTest(TestCase):
    """ Test module for updating an existing service area record """

    def setUp(self):
        self.service_area_1 = ServiceArea.objects.create(
            name="Service Area 1",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="UPS",
                email="ups@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

        self.service_area_2 = ServiceArea.objects.create(
            name="Service Area 2",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="DHL",
                email="dhl@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

        self.valid_payload = {
            "name": "Service Area 1",
            "price": 10,
            "area": "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            "provider": Provider.objects.create(
                name="UPS",
                email="ups@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            ).pk
        }

        self.invalid_payload = {
            "name": "Service Area 1",
            "price": 10,
            "area": "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            "provider": 30,
        }

    def test_valid_update_service_area(self):
        response = client.put(
            reverse('get_delete_update_service_area', kwargs={'pk': self.service_area_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_service_area(self):
        response = client.put(
            reverse('get_delete_update_service_area', kwargs={'pk': self.service_area_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleServiceAreaTest(TestCase):
    """ Test module for deleting an existing service area record """

    def setUp(self):
        self.service_area_1 = ServiceArea.objects.create(
            name="Service Area 1",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="UPS",
                email="ups@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

        self.service_area_2 = ServiceArea.objects.create(
            name="Service Area 2",
            price=10,
            area="POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))",
            provider=Provider.objects.create(
                name="DHL",
                email="dhl@gmail.com",
                phone_number="1234567890",
                language="English",
                currency="USD"
            )
        )

    def test_valid_delete_service_area(self):
        response = client.delete(
            reverse('get_delete_update_service_area', kwargs={'pk': self.service_area_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_service_area(self):
        response = client.delete(
            reverse('get_delete_update_service_area', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
