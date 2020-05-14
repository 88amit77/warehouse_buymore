from django.db import models


# Create your models here.
class WarehouseDetails(models.Model):
    warehouse_code = models.CharField(max_length=50)
    warehouse_address = models.CharField(max_length=50)
    warehouse_latitude = models.CharField(max_length=50)
    warehouse_longitude = models.CharField(max_length=50)
    gst_number = models.CharField(max_length=100)
    cubic_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    racked_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    unracked_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    inward_zone_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    numbered_outward_stations = models.IntegerField()
    loading_doc_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    current_cubic_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    location_id = models.IntegerField(default=0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
