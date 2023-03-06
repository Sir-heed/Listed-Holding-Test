from django.contrib.auth import get_user_model
from django_filters import rest_framework as df_filters

class UserFilter(df_filters.FilterSet):
    class Meta:
        model = get_user_model()
        fields = ['is_active', 'user_type']