from django.contrib.auth import get_user_model
from django_filters import rest_framework as df_filters

from parcel.models import Parcel

class ParcelFilter(df_filters.FilterSet):
    title = df_filters.CharFilter(field_name="title", lookup_expr="icontains")
    class Meta:
        model = Parcel
        fields = ['delivery_status', 'title']