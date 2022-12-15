from django.shortcuts   import render, redirect
from django.http        import HttpResponse, HttpResponseRedirect

from core.models        import Customer, Product, Manager, WholesaleCompany, Clerk, DiscountService, AccumulatingService
from core.models        import SellingBill, SellingBillDetail, RestockingBill, RestockingBillDetail

from datetime           import datetime
from random             import randint

def index(request):
    context = {}

    return render(request, 'manager/index.html', context)

def restock(request):
    context = {}

    return render(request, 'manager/restock.html', context)

def restock_calc_bill(request):
    context = {}

    total_price = 0
    final_price = 0

    wholesale_company = WholesaleCompany.objects.get(pk = request.POST['WCName'])

    context['wc_name'] = wholesale_company.WCName
    context['m_no'] = request.POST['MNo']
    context['product'] = {}

    iterator = '0'
    while ('PBarcode' + iterator) in request.POST.keys():
        context['product'][iterator] = {}

        product = Product.objects.get(pk = request.POST['PBarcode' + iterator])
        p_name = product.PName
        p_price = int(product.PPrice * 70 // 100 // 1000 * 1000)
        rb_price = p_price * int(request.POST['RBQty' + iterator])
        total_price += rb_price

        context['product'][iterator]['p_barcode'] = request.POST['PBarcode' + iterator]
        context['product'][iterator]['rb_qty'] = request.POST['RBQty' + iterator]
        context['product'][iterator]['p_name'] = p_name
        context['product'][iterator]['p_price'] = p_price
        context['product'][iterator]['rb_price'] = rb_price
        iterator = str(int(iterator) + 1)

    final_price = int(total_price // 1000 * 1000)

    context['num_products'] = int(iterator)
    context['total_price'] = int(total_price)
    context['final_price'] = int(final_price)

    print(context)
    
    request.session['context'] = context
    return HttpResponseRedirect('../restock', context)

def restock_submit_bill(request):
    context = {
        'num_products': 0,
        'products': {},
        'total_price': 0,
        'final_price': 0
    }

    print(request.POST)
    wholesale_company = WholesaleCompany.objects.get(pk = request.POST['WCName'])
    manager = Manager.objects.get(pk = request.POST['MNo'])

    iterator = '0'
    total_price = 0

    while ('PBarcode' + iterator) in request.POST.keys():
        product = Product.objects.get(pk = request.POST['PBarcode' + iterator])
        product.PQty += int(request.POST['RBQty' + iterator])
        product.save()

        p_price = int(product.PPrice * 70 // 100 // 1000 * 1000)
        rb_price = p_price * int(request.POST['RBQty' + iterator])
        total_price += rb_price

        iterator = str(int(iterator) + 1)

    final_price = int(total_price // 1000 * 1000)

    rb_no = str(randint(1000000000, 9999999999))

    try:
        RestockingBill.objects.get(pk = rb_no)
    except:
        restocking_bill = RestockingBill.objects.create(
            RBNo = rb_no,
            MNo = manager,
            WCName = wholesale_company,
            RBDate = datetime.now(),
            RBPrice = final_price
        )

        restocking_bill.save()

        iterator = '0'
        while ('PBarcode' + iterator) in request.POST.keys():
            product = Product.objects.get(pk = request.POST['PBarcode' + iterator])
            restocking_bill_detail = RestockingBillDetail.objects.create(
                RBNo = restocking_bill,
                PBarcode = product,
                RBWPrice = product.PPrice * 70 // 100 // 1000 * 1000,
                RBQty = int(request.POST['RBQty' + iterator])
            )
            print(restocking_bill_detail.RBQty)
            restocking_bill_detail.save()
            iterator = str(int(iterator) + 1)
    else:
        pass
    finally:
        request.session['context'] = context
        return HttpResponseRedirect('../restock', context)

def manage_info_clerk(request):
    context = {}
    lst_clerks = Clerk.objects.all()
    context['lst_clerks'] = lst_clerks

    return render(request, 'manager/clerk.html', context)

def manage_info_product(request):
    context = {}
    lst_products = Product.objects.all()
    context['lst_product'] = lst_products

    return render(request, 'manager/product.html', context)

def manage_info_wholesale_company(request):
    context = {}
    lst_wholesale_companies = WholesaleCompany.objects.all()
    context['lst_wholesale_companies'] = lst_wholesale_companies

    return render(request, 'manager/wholesale.html', context)

def manage_info_discount_service(request):
    context = {}
    lst_discount_service = DiscountService.objects.all()
    context['lst_discount_service'] = lst_discount_service

    return render(request, 'manager/discount.html', context)

def manage_info_accumulating_service(request):
    context = {}
    lst_accumulating_service = AccumulatingService.objects.all()
    context['lst_accumulating_service'] = lst_accumulating_service

    return render(request, 'manager/accumulation.html', context)

def manage_info_customer(request):
    context = {}
    lst_customer = Customer.objects.all()
    context['lst_customer'] = lst_customer

    return render(request, 'manager/customer.html', context)

def manage_info_restocking_bill(request):
    context = {}
    lst_restocking_bill = RestockingBill.objects.all()
    context['lst_restocking_bill'] = lst_restocking_bill

    return render(request, 'manager/restockingBill.html', context)

def manage_info_selling_bill(request):
    context = {}
    lst_selling_bill = SellingBill.objects.all()
    lst_selling_bill_detail = SellingBillDetail.objects.all()

    context['lst_selling_bill'] = lst_selling_bill
    context['lst_selling_bill_detail'] = lst_selling_bill_detail

    return render(request, 'manager/sellingBill.html', context)
    
def manage_info_clerk_add(request):
    try:
        Clerk.objects.get(pk = request.POST['ClNo'])
    except:
        Clerk.objects.create(
            ClNo = request.POST['ClNo'],
            ClName = request.POST['ClName'],
            ClAddress = request.POST['ClAddress'],
            ClPhoneNo = request.POST['ClPhoneNo'],
            ClWorkShift = request.POST['ClWorkShift'],
            ClSalary = request.POST['ClSalary'],
        )
        context = {'mes': ''}
    else:
        context = {'mes': 'Clerk number already exists'}
    finally:
        return HttpResponseRedirect('../clerk', context)

def manage_info_wholesale_company_add(request):
    try: 
        WholesaleCompany.objects.get(pk = request.POST['WCName'])
    except:
        WholesaleCompany.objects.create(
            WCName = request.POST['WCName'],
            WCAddress = request.POST['WCAddress'],
            WCPhoneNo = request.POST['WCPhoneNo'],
        )
        context = {'mes': ''}
    else:
        context = {'mes': 'Company already exists'}
    finally:
        return HttpResponseRedirect('../wholesale_company', context)

def manage_info_clerk_delete(request):
    try:
        clerk = Clerk.objects.get(pk = request.POST['ClNo'])
    except:
        context = {'mes': 'Clerk does not exist'}
    else:
        clerk.delete()

        context = {'mes': ''}
    finally:
        return HttpResponseRedirect('../clerk', context)

def manage_info_wholesale_company_delete(request):
    try:
        wc = WholesaleCompany.objects.get(pk = request.POST['WCName'])
    except:
        context = {'mes': 'Wholesale company does not exist'}
    else:
        wc.delete()

        context = {'mes': ''}
    finally:
        return HttpResponseRedirect('../wholesale_company', context)