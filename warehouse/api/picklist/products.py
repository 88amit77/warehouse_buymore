from django.db import models


class AmazonAmazonproducts(models.Model):
    amazon_product_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    amazon_portal_sku = models.CharField(max_length=50)
    amazon_unique_id = models.CharField(max_length=50)
    amazon_listing_id = models.CharField(max_length=50)
    amazon_price_rule = models.IntegerField()
    amazon_break_even_sp = models.FloatField()
    amazon_min_break_even_sp = models.FloatField()
    amazon_max_break_even_sp = models.FloatField()
    amazon_vendors_price = models.FloatField()
    amazon_purchase_order_value = models.FloatField()
    amazon_current_selling_price = models.FloatField()
    amazon_upload_selling_price = models.FloatField()
    amazon_competitor_lowest_price = models.FloatField()
    amazon_account_id = models.IntegerField()
    amazon_all_values_external_api = models.CharField(max_length=50)
    amazon_created_at = models.DateTimeField()
    amazon_updated_at = models.DateTimeField()
    amazon_portal_category = models.ForeignKey('CalculationCategorycommission', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_amazonproducts'


class CalculationCategorycommission(models.Model):
    category_commision_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=100)
    commission_rate = models.FloatField()
    depend_price = models.TextField()  # This field type is a guess.
    is_applicable = models.BooleanField()
    multi_portal_id = models.SmallIntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category_reqmt = models.ForeignKey('CalculationCategoryrequirement', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calculation_categorycommission'


class CalculationCategoryrequirement(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=145)
    default_commission_rate = models.FloatField()
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField(blank=True, null=True)
    max = models.IntegerField()
    min = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_categoryrequirement'


class CalculationCurrency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=100)
    currency_value = models.FloatField()
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_currency'


class CalculationDependprice(models.Model):
    depend_price_id = models.AutoField(primary_key=True)
    depend_price_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_dependprice'


class CalculationHsncoderate(models.Model):
    hsn_rate_id = models.AutoField(primary_key=True)
    hsn_code = models.CharField(max_length=50)
    max_rate = models.FloatField()
    min_rate = models.FloatField()
    threshold_amount = models.IntegerField()
    depend_price = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_hsncoderate'


class CalculationMasterothercommission(models.Model):
    charge_id = models.AutoField(primary_key=True)
    charge_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_masterothercommission'


class CalculationOthercommission(models.Model):
    charge_name = models.CharField(max_length=50)
    portal_id = models.IntegerField()
    charge_value = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    expiry_date = models.DateField()
    depend_price_id = models.ForeignKey(CalculationDependprice, models.DO_NOTHING)
    othccharge_id = models.ForeignKey(CalculationMasterothercommission, models.DO_NOTHING)
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calculation_othercommission'


class CalculationPricerule(models.Model):
    price_rule_id = models.AutoField(primary_key=True)
    price_rule_code = models.CharField(max_length=100)
    percentage_value = models.FloatField(blank=True, null=True)
    price_rule_type = models.IntegerField()
    list_value = models.CharField(max_length=50)
    percentage_price_list = models.IntegerField(blank=True, null=True)
    user_type = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_pricerule'


class CalculationRequirementcalculation(models.Model):
    requirement_id = models.AutoField(primary_key=True)
    calculation_using_formula = models.BooleanField()
    thirty_days = models.BooleanField()
    sixty_days = models.BooleanField()
    ninety_days = models.BooleanField()
    one_twenty_days = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_requirementcalculation'


class CalculationWeighthandling(models.Model):
    weight_handling_charge_id = models.AutoField(primary_key=True)
    weight_handling_type = models.SmallIntegerField()
    max_weight = models.FloatField()
    fixed_weight = models.FloatField()
    national_fixed_weight_value = models.FloatField()
    value_after_national_fixed_weight = models.FloatField()
    zonal_fixed_weight_value = models.FloatField()
    value_after_zonal_fixed_weight = models.FloatField()
    local_fixed_weight_value = models.FloatField()
    value_after_local_fixed_weight = models.FloatField()
    weight_limit = models.FloatField()
    national_reverse_shipping_charge = models.FloatField()
    zonal_reverse_shipping_charge = models.FloatField()
    local_reverse_shipping_charge = models.FloatField()
    from_date = models.DateField()
    to_date = models.DateField()
    multiple_portal_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calculation_weighthandling'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DynamicFormulaDyproducts(models.Model):
    flip_product_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    fli_portal_sku = models.CharField(max_length=50)
    fli_portal_unique_id = models.CharField(max_length=50)
    flip_listing_id = models.CharField(max_length=50)
    flip_price_rule = models.IntegerField()
    flip_break_even_sp = models.FloatField()
    flip_min_break_even_sp = models.FloatField()
    flip_max_break_even_sp = models.FloatField()
    flip_vendors_price = models.FloatField()
    flip_purchase_order_value = models.FloatField()
    fli_current_selling_price = models.FloatField()
    fli_upload_selling_price = models.FloatField()
    fli_competitor_lowest_price = models.FloatField()
    flip_account_id = models.IntegerField()
    flip_all_values_external_api = models.CharField(max_length=50)
    flip_portal_category = models.ForeignKey(CalculationCategorycommission, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dynamic_formula_dyproducts'


class FlipkartFlipkartproducts(models.Model):
    flipkart_product_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    flipkart_portal_sku = models.CharField(max_length=50)
    flipkart_portal_unique_id = models.CharField(max_length=50)
    flipkart_listing_id = models.CharField(max_length=50)
    flipkart_price_rule = models.IntegerField()
    flipkart_break_even_sp = models.FloatField()
    flipkart_min_break_even_sp = models.FloatField()
    flipkart_max_break_even_sp = models.FloatField()
    flipkart_vendors_price = models.FloatField()
    flipkart_purchase_order_value = models.FloatField()
    flipkart_current_selling_price = models.FloatField()
    flipkart_upload_selling_price = models.FloatField()
    flipkart_competitor_lowest_price = models.FloatField()
    flipkart_account_id = models.IntegerField()
    flipkart_all_values_external_api = models.CharField(max_length=50)
    flipkart_portal_category = models.ForeignKey(CalculationCategorycommission, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flipkart_flipkartproducts'


class FlipkartFpktCsv(models.Model):
    fpkt_csv_id = models.AutoField(primary_key=True)
    csv_filename = models.CharField(max_length=100)
    csv_import = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'flipkart_fpkt_csv'


class MasterBrand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    description = models.TextField()
    vendor_id = models.SmallIntegerField()
    warehouse_id = models.SmallIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_brand'


class MasterMasterproduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    buymore_sku = models.CharField(max_length=100)
    ean = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_mrp = models.SmallIntegerField()
    product_length = models.FloatField()
    product_breath = models.FloatField()
    product_width = models.FloatField()
    product_weight = models.FloatField()
    min_payout_value = models.FloatField()
    max_payout_value = models.FloatField()
    product_model_no = models.CharField(max_length=50)
    series_name = models.CharField(max_length=50)
    child_variations = models.SmallIntegerField()
    description = models.CharField(max_length=255)
    sales_rank = models.IntegerField()
    image_url = models.CharField(max_length=200)
    key_point = models.CharField(max_length=145)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    brand_id = models.ForeignKey(MasterBrand, models.DO_NOTHING)
    category_id = models.ForeignKey(CalculationCategoryrequirement, models.DO_NOTHING)
    currency_id = models.ForeignKey(CalculationCurrency, models.DO_NOTHING)
    hsn_code_id = models.ForeignKey(CalculationHsncoderate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'master_masterproduct'


class MasterPortalaccount(models.Model):
    portal_id = models.AutoField(primary_key=True)
    portal_name = models.CharField(max_length=50)
    portal_icon = models.CharField(max_length=100)
    authentication_attributes = models.TextField()  # This field type is a guess.
    api_list_with_base_url = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'master_portalaccount'


class MasterPortalaccountdetails(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    authentication_attribute_values = models.TextField()  # This field type is a guess.
    warehouse_connection_values = models.TextField()  # This field type is a guess.
    portal_id = models.ForeignKey(MasterPortalaccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'master_portalaccountdetails'


class MasterProductattribute(models.Model):
    product_attribute_id = models.AutoField(primary_key=True)
    asin = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    item_height = models.FloatField()
    item_length = models.FloatField()
    item_width = models.FloatField()
    item_weight = models.FloatField()
    label = models.CharField(max_length=50)
    manufacturers = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    package_height = models.FloatField()
    package_length = models.FloatField()
    package_width = models.FloatField()
    package_weight = models.FloatField()
    package_quantity = models.FloatField()
    part_number = models.CharField(max_length=50)
    product_group = models.CharField(max_length=50)
    product_type_name = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    image_height = models.FloatField()
    image_width = models.FloatField()
    studio = models.CharField(max_length=50)
    title = models.TextField()
    number_of_images = models.IntegerField()
    image_1 = models.CharField(max_length=200)
    image_2 = models.CharField(max_length=200)
    image_3 = models.CharField(max_length=200)
    image_4 = models.CharField(max_length=200)
    image_5 = models.CharField(max_length=200)
    image_6 = models.CharField(max_length=200)
    number_of_key_points = models.IntegerField()
    key_point_1 = models.TextField()
    key_point_2 = models.TextField()
    key_point_3 = models.TextField()
    key_point_4 = models.TextField()
    key_point_5 = models.TextField()
    key_point_6 = models.TextField()
    browse_node = models.CharField(max_length=50)
    selling_price = models.FloatField()
    mrp = models.FloatField()
    product_rating = models.FloatField()
    customer_review = models.TextField()
    buy_box_seller_name = models.CharField(max_length=50)
    buy_box_seller_rating = models.FloatField()
    description = models.TextField()
    multiple_portal_id = models.IntegerField()
    sales_rank = models.IntegerField()
    sales_rank_category = models.IntegerField()
    seller_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    product_id = models.ForeignKey(MasterMasterproduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'master_productattribute'


class MasterStockrequirement(models.Model):
    stock_requirement_id = models.AutoField(primary_key=True)
    requirement = models.IntegerField()
    balance_requirement = models.IntegerField()
    excess_stock = models.IntegerField()
    final_requirement_value = models.IntegerField()
    east_zone_requirement = models.IntegerField()
    west_zone_requirement = models.IntegerField()
    north_zone_requirement = models.IntegerField()
    south_zone_requirement = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    product_id = models.ForeignKey(MasterMasterproduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'master_stockrequirement'


class PaytmPaytmproducts(models.Model):
    paytm_product_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    paytm_portal_sku = models.CharField(max_length=50)
    paytm_portal_unique_id = models.FloatField()
    paytm_listing_id = models.CharField(max_length=50)
    paytm_price_rule = models.IntegerField()
    paytm_break_even_sp = models.FloatField()
    paytm_min_break_even_sp = models.FloatField()
    paytm_max_break_even_sp = models.FloatField()
    paytm_vendors_price = models.FloatField()
    paytm_purchase_order_value = models.FloatField()
    paytm_current_selling_price = models.FloatField()
    paytm_upload_selling_price = models.FloatField()
    paytm_competitor_lowest_price = models.FloatField()
    paytm_account_id = models.IntegerField()
    paytm_all_values_external_api = models.CharField(max_length=50)
    paytm_portal_category = models.ForeignKey(CalculationCategorycommission, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paytm_paytmproducts'


class PaytmPtmCsv(models.Model):
    ptm_csv_id = models.AutoField(primary_key=True)
    csv_filename = models.CharField(max_length=100)
    csv_import = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'paytm_ptm_csv'


class PurchaseInvoicePurchaseinvoices(models.Model):
    purchase_invoice_id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateTimeField()
    purchase_order_number = models.IntegerField()
    vendor_id = models.IntegerField()
    payment_due_date = models.DateField()
    userid_to_verify = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    invoice_upload = models.CharField(max_length=100, blank=True, null=True)
    invoice_kind = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_invoice_purchaseinvoices'


class PurchaseInvoicePurchaseskudetails(models.Model):
    purchase_details_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    basic_price = models.FloatField()
    net_gst = models.FloatField()
    is_calculated = models.BooleanField()
    po_value = models.FloatField()
    is_below_po = models.BooleanField()
    qty_received = models.IntegerField()
    purchase_invoice_id = models.ForeignKey(PurchaseInvoicePurchaseinvoices, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'purchase_invoice_purchaseskudetails'
