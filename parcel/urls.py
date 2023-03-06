from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ParcelViewSets)

app_name = 'parcel'

router = DefaultRouter()
router.register('parcels', ParcelViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
