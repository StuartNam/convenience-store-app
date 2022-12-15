from django.urls        import path
from .                  import views

app_name = 'clerk'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('sell', views.sell, name = 'sell'),
    path('sell/add_new_customer', views.add_new_customer, name = 'add_new_customer'),
    path('sell/calc_bill', views.calc_bill, name = 'calc_bill'),
    path('sell/submit_bill', views.submit_bill, name = 'submit_bill')
]