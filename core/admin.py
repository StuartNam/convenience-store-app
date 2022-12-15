from django.contrib import admin
from .models        import Clerk, Customer, Product, WholesaleCompany, Manager, DiscountService, AccumulatingService
from .models        import SellingBill, SellingBillDetail, RestockingBill, RestockingBillDetail

admin.site.register(Clerk)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(WholesaleCompany)
admin.site.register(Manager)
admin.site.register(DiscountService)
admin.site.register(AccumulatingService)
admin.site.register(SellingBill)
admin.site.register(SellingBillDetail)
admin.site.register(RestockingBill)
admin.site.register(RestockingBillDetail)
