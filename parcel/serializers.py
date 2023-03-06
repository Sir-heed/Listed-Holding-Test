from rest_framework import serializers

from parcel.models import Parcel

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'
        read_only_fields = ['created_by', 'delivery_status']


class CancelParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ['delivery_status']