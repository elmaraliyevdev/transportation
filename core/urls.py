from .views import ProviderViewSet, ServiceAreaViewSet
from rest_framework.routers import DefaultRouter

app_name = 'core'

router = DefaultRouter()

router.register('provider', ProviderViewSet, basename='provider')
router.register('service-area', ServiceAreaViewSet, basename='service-area')

urlpatterns = router.urls
