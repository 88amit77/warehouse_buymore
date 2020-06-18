from django.db import models


class ApiDispatchdetails(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    pincode = models.IntegerField()
    location_latitude = models.FloatField()
    location_longitude = models.FloatField()
    email_id = models.CharField(max_length=254)
    phone = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    l_b_h_w = models.CharField(max_length=50)
    bin_id = models.IntegerField(db_column='bin_Id')  # Field name made lowercase.
    picklist_id = models.IntegerField()
    is_mark_placed = models.BooleanField()
    have_invoice_file = models.BooleanField()
    packing_status = models.BooleanField()
    is_dispatch = models.BooleanField()
    dispatch_confirmed = models.BooleanField()
    is_shipment_create = models.BooleanField()
    awb = models.CharField(max_length=30, blank=True, null=True)
    courier_partner = models.CharField(max_length=30)
    shipment_id = models.IntegerField()
    is_canceled = models.BooleanField()
    cancel_inward_bin = models.CharField(max_length=30)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()
    dd_id = models.ForeignKey('ApiNeworder', models.DO_NOTHING, blank=True, null=True)
    mf_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_dispatchdetails'


class ApiFulfilledreturn(models.Model):
    fr_id = models.AutoField(primary_key=True)
    return_request_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    destination_warehouse_id = models.IntegerField()
    return_reason = models.CharField(max_length=70)
    sub_reason = models.CharField(max_length=50)
    awb = models.CharField(max_length=40)
    return_type = models.CharField(max_length=20)
    dd_id = models.ForeignKey('ApiNeworder', models.DO_NOTHING, blank=True, null=True)
    pod_id = models.ForeignKey('ApiPodlist', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_fulfilledreturn'


class ApiManifest(models.Model):
    mf_id = models.AutoField(primary_key=True)
    courier_partner = models.CharField(max_length=20)
    mf_sheet = models.CharField(max_length=200)
    created_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'api_manifest'


class ApiManifestAwb(models.Model):
    manifest = models.ForeignKey(ApiManifest, models.DO_NOTHING)
    dispatchdetails = models.ForeignKey(ApiDispatchdetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_manifest_awb'
        unique_together = (('manifest', 'dispatchdetails'),)


class ApiNeworder(models.Model):
    buymore_order_id = models.AutoField(primary_key=True)
    dd_id = models.IntegerField()
    product_id = models.IntegerField()
    order_id = models.IntegerField()
    order_item_id = models.IntegerField()
    order_date = models.DateField()
    dispatch_by_date = models.DateField()
    portal_id = models.IntegerField()
    portal_sku = models.CharField(max_length=30)
    qty = models.IntegerField()
    selling_price = models.FloatField()
    mrp = models.FloatField()
    tax_rate = models.FloatField()
    warehouse_id = models.IntegerField()
    region = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'api_neworder'


class ApiPodlist(models.Model):
    pod_id = models.AutoField(primary_key=True)
    pod_number = models.CharField(max_length=20)
    courier_partner_name = models.CharField(max_length=30)
    pod_image_list = models.CharField(max_length=200, blank=True, null=True)
    total_quantity_received = models.IntegerField()
    processed_quantity = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    courier_received_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_podlist'


class ApiRefundimagetable(models.Model):
    image_list = models.CharField(max_length=200)
    return_category = models.CharField(max_length=50)
    return_notes = models.CharField(max_length=50)
    tracking_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    processing_date = models.DateTimeField(blank=True, null=True)
    return_type = models.CharField(max_length=50)
    package_condition = models.CharField(max_length=50)
    is_barcode_required = models.BooleanField()
    product_condition = models.CharField(max_length=50)
    image_correctness = models.BooleanField()
    size_correctness = models.BooleanField()
    alternate_product_id = models.IntegerField(blank=True, null=True)
    sellable = models.BooleanField()
    dd_id = models.ForeignKey(ApiNeworder, models.DO_NOTHING, blank=True, null=True)
    pod_id = models.ForeignKey(ApiPodlist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_refundimagetable'


class ApiReimburesement(models.Model):
    rr_id = models.AutoField(primary_key=True)
    case_id = models.CharField(max_length=20)
    status_of_case = models.CharField(max_length=20)
    case_content = models.CharField(max_length=20)
    case_reply = models.CharField(max_length=20)
    reimbursement_amount = models.FloatField()
    dd_id = models.ForeignKey(ApiNeworder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_reimburesement'


class ApiReimbursement(models.Model):
    rr_id = models.AutoField(primary_key=True)
    case_id = models.CharField(max_length=20)
    status_of_case = models.CharField(max_length=20)
    case_content = models.CharField(max_length=20)
    case_reply = models.CharField(max_length=20)
    reimbursement_amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'api_reimbursement'


class ApiReimbursementDdId(models.Model):
    reimbursement = models.ForeignKey(ApiReimbursement, models.DO_NOTHING)
    neworder = models.ForeignKey(ApiNeworder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_reimbursement_dd_id'
        unique_together = (('reimbursement', 'neworder'),)
