from django.db import models

class DiscountService(models.Model):
    ds_tier = models.CharField(
        name = 'DSTier',
        max_length = 7,
        primary_key = True
    )

    ds_rate = models.IntegerField(
        name = 'DSRate'
    )

    ds_maxpoint = models.IntegerField(
        name = 'DSMaxPoint',
        default = 1
    )

class WholesaleCompany(models.Model):
    wc_name = models.CharField(
        name = 'WCName',
        max_length = 100,
        primary_key = True
    )

    wc_address = models.CharField(
        name = 'WCAddress',
        max_length = 100
    )

    wc_phone_no = models.CharField(
        name = 'WCPhoneNo',
        max_length = 11
    )

class Product(models.Model):
    p_barcode = models.CharField(
        name = 'PBarcode',
        max_length = 13,
        primary_key = True
    )

    p_name = models.CharField(
        name = 'PName',
        max_length = 100
    )

    p_quantity = models.IntegerField(
        name = 'PQty'
    )

    p_price = models.IntegerField(
        name = 'PPrice'
    )

    p_discount_rate = models.IntegerField(
        name = 'PDiscountRate',
        null = True
    )

    wc_name = models.ForeignKey(
        WholesaleCompany,
        name = 'WCName',
        on_delete = models.CASCADE,
        default = ""
    )

class Clerk(models.Model):
    cl_no = models.CharField(
        name = 'ClNo',
        max_length = 10,
        primary_key = True
    )

    cl_name = models.CharField(
        name = 'ClName',
        max_length = 100
    )

    cl_address = models.CharField(
        name = 'ClAddress',
        max_length = 100
    )

    cl_phone_no = models.CharField(
        name = 'ClPhoneNo',
        max_length = 11
    )

    cl_work_shift = models.IntegerField(
        name = 'ClWorkShift'
    )

    cl_salary = models.IntegerField(
        name = 'ClSalary'
    )

class Customer(models.Model):
    c_phone_no = models.CharField(
        name = 'CPhoneNo',
        max_length = 11,
        primary_key = True
    )

    c_name = models.CharField(
        name = 'CName',
        max_length = 100
    )

    c_address = models.CharField(
        name = 'CAddress',
        max_length = 100
    )

    c_tier = models.ForeignKey(
        DiscountService,
        name = 'CTier',
        on_delete = models.CASCADE
    )

    c_point = models.IntegerField(
        name = 'CPoint'
    )

    c_deduction_date = models.DateField(
        name = 'CDeductionDate'
    )

    products = models.ManyToManyField(
        Product,
        through = 'AccumulatingService'
    )

class Manager(models.Model):
    m_no = models.CharField(
        name = 'MNo',
        max_length = 10,
        primary_key = True
    )

    m_name = models.CharField(
        name = 'MName',
        max_length = 100
    )

    m_address = models.CharField(
        name = 'MAddress',
        max_length = 100
    )

    m_phone_no = models.CharField(
        name = 'MPhoneNo',
        max_length = 11
    )

    m_salary = models.IntegerField(
        name = 'MSalary'
    )

    m_bonus = models.IntegerField(
        name = 'MBonus'
    )  

class AccumulatingService(models.Model):
    p_barcode = models.OneToOneField(
        Product,
        name = 'PBarcode',
        on_delete = models.CASCADE,
        primary_key = True
    )

    c_phone_no = models.ForeignKey(
    Customer,
    name = 'CPhoneNo',
    on_delete = models.CASCADE
    )

    as_no_stamps = models.IntegerField(
        name = 'ASNoStamps'
    )

    as_min_stamps = models.IntegerField(
        name = 'ASMinStamps',
        default = 1
    )

class SellingBill(models.Model):
    sb_no = models.CharField(
        name = 'SBNo',
        max_length = 10,
        primary_key = True
    )

    cl_no = models.ForeignKey(
        Clerk,
        name = 'ClNo',
        on_delete = models.CASCADE
    )

    c_phone_no = models.ForeignKey(
        Customer,
        name = 'CPhoneNo',
        on_delete = models.CASCADE
    )

    sb_date = models.DateTimeField(
        name = 'SBDate'
    )

    sb_price = models.IntegerField(
        name = 'SBPrice'
    )

    products = models.ManyToManyField(
        Product,
        through = 'SellingBillDetail'
    )

class SellingBillDetail(models.Model):
    sb_no = models.ForeignKey(
        SellingBill,
        name = 'SBNo',
        on_delete = models.CASCADE
    )

    p_barcode = models.ForeignKey(
        Product,
        name = 'PBarcode',
        on_delete = models.CASCADE
    )

    sb_qty = models.IntegerField(
        name = 'SBQty'
    )

class RestockingBill(models.Model):
    rb_no = models.CharField(
        name = 'RBNo',
        max_length = 10,
        primary_key = True
    )

    m_no = models.ForeignKey(
        Manager,
        name = 'MNo',
        on_delete = models.CASCADE
    )

    wc_name = models.ForeignKey(
        WholesaleCompany,
        name = 'WCName',
        on_delete = models.CASCADE
    )

    rb_date = models.DateTimeField(
        name = 'RBDate'
    )

    rb_price = models.IntegerField(
        name = 'RBPrice'
    )

    products = models.ManyToManyField(
        Product,
        through = 'RestockingBillDetail'
    )

class RestockingBillDetail(models.Model):
    rb_no = models.ForeignKey(
        RestockingBill,
        name = 'RBNo',
        on_delete = models.CASCADE
    )

    p_barcode = models.ForeignKey(
        Product,
        name = 'PBarcode',
        on_delete = models.CASCADE
    )

    rb_wholesale_price = models.IntegerField(
        name = 'RBWPrice'
    )

    rb_qty = models.IntegerField(
        name = 'RBQty'
    )