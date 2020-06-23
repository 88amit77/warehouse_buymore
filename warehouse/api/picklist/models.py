from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Picklist(models.Model):
    picklist_id = models.CharField(max_length=30)
    total_orders = models.IntegerField()
    shipout_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    portals = ArrayField(models.IntegerField(), blank=True)
    quantity = models.IntegerField()
    warehouse_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class PicklistItems(models.Model):
    picklist_id = models.IntegerField()
    portal_new_order_id = models.IntegerField()
    status = models.CharField(max_length=50)
    found = models.CharField(max_length=50)
    remarks = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)


class PicklistItemAlternate(models.Model):
    picklist_item_id = models.IntegerField()
    product_id = models.IntegerField()


class PicklistAssignee(models.Model):
    user_id = models.IntegerField()
    picklist_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class PicklistItemProcessing(models.Model):
    picklist_item_id = models.IntegerField()
    size_correctness = models.BooleanField()
    size_remarks = models.TextField(null=True, blank=True)
    image_correctness = models.BooleanField()
    image_remarks = models.TextField(null=True, blank=True)
    title_correctness = models.BooleanField()
    title_remarks = models.TextField(null=True, blank=True)
    dimension_correctness = models.BooleanField()
    dimension_remarks = models.TextField(null=True, blank=True)
    product_condition = models.BooleanField()
    product_condition_remarks = models.TextField(null=True, blank=True)
    status = models.BooleanField()
    status_remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PicklistProcessingMonitor(models.Model):
    picklist_id = models.IntegerField()
    picklist_file = models.TextField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    items_processed = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)

