from django.urls        import path
from .                  import views

app_name = 'manager'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('restock', views.restock, name = 'restock'),
    path('restock/calc_bill', views.restock_calc_bill, name = 'restock_salc_bill'),
    path('restock/submit_bill', views.restock_submit_bill, name = 'restock_submit_bill'),
    path('manage_info/clerk', views.manage_info_clerk, name = 'manage_info_clerk'),
    path('manage_info/customer', views.manage_info_customer, name = 'manage_info_customer'),
    path('manage_info/product', views.manage_info_product, name = 'manage_info_product'),
    path('manage_info/discount_service', views.manage_info_discount_service, name = 'manage_info_discount_service'),
    path('manage_info/accumulating_service', views.manage_info_accumulating_service, name = 'manage_info_accumulating_servie'),
    path('manage_info/wholesale_company', views.manage_info_wholesale_company, name = 'manage_info_wholesale_company'),
    path('manage_info/restocking_bill', views.manage_info_restocking_bill, name = 'manage_info_restocking_bill'),
    path('manage_info/selling_bill', views.manage_info_selling_bill, name = 'manage_info_selling_bill'),
    path('manage_info/clerk/add', views.manage_info_clerk_add, name = 'manage_info_clerk_add'),
    path('manage_info/wholesale_company/add', views.manage_info_wholesale_company_add, name = 'manage_info_wholesale_company_add'),
    path('manage_info/clerk/delete', views.manage_info_clerk_delete, name = 'manage_info_clerk_delete'),
    path('manage_info/wholesale_company/delete', views.manage_info_wholesale_company_delete, name = 'manage_info_wholesale_company_delete'),
]