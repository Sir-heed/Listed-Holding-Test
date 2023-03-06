from django.db import models
from lhtest.models import AuditableModel
from parcel.enums import DELIVERY_STATUS
from user.models import User

# Create your models here.
class Parcel(AuditableModel):
    title = models.CharField(max_length=250)
    weight = models.FloatField()
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='PENDING')
    amount = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parcels')

    def __str__(self) -> str:
        return self.title