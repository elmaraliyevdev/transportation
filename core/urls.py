from django.urls import path
from . import views

urlpatterns = [
    path('api/providers/<int:pk>', views.get_delete_update_provider, name='get_delete_update_provider'),
    path('api/providers/', views.get_post_providers, name='get_post_providers'),
    path('api/service-areas/<int:pk>', views.get_delete_update_service_area, name='get_delete_update_service_area'),
    path('api/service-areas/', views.get_post_service_areas, name='get_post_service_areas'),
    path('api/get-service-areas-by-point/', views.get_service_areas_by_point, name='get_service_areas_by_point'),
]
