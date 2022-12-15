from django.shortcuts   import render
from django.http        import HttpResponse, HttpResponseRedirect

from core.models        import Customer, Product, Manager, WholesaleCompany, Clerk, DiscountService, AccumulatingService
from core.models        import SellingBill, SellingBillDetail, RestockingBill, RestockingBillDetail

from datetime           import datetime
from random             import randint

def index(request):
    context = {}

    return render(request, 'clerk/index.html', context)

def sell(request, context = {'num_products': 0}):
    return render(request, 'clerk/sell.html', context)

def add_new_customer(request):
    customer = Customer.objects.create(
        CPhoneNo = request.POST['CPhoneNo'],
        CName = request.POST['CName'],
        CAddress = request.POST['CAddress'],
        CTier = DiscountService.objects.get(pk = 'WOODEN'),
        CPoint = 0,
        CDeductionDate = "2024-01-01"
    )

    customer.save()

    return HttpResponseRedirect('../sell')

def calc_bill(request):
    context = {}

    c_discount_rate = 0
    total_price = 0
    final_price = 0

    customer = Customer.objects.select_related('CTier').get(pk = request.POST['CPhoneNo'])
    c_discount_rate = customer.CTier.DSRate
    context['c_discount_rate'] = c_discount_rate
    context['c_phone_no'] = customer.CPhoneNo
    context['cl_no'] = request.POST['ClNo']
    context['product'] = {}
    iterator = '0'
    
    while ('PBarcode' + iterator) in request.POST.keys():
        context['product'][iterator] = {}

        product = Product.objects.get(pk = request.POST['PBarcode' + iterator])
        p_name = product.PName
        p_price = int(product.PPrice * (100 - product.PDiscountRate) // 100 // 1000 * 1000)
        sb_price = p_price * int(request.POST['SBQty' + iterator])
        total_price += sb_price

        context['product'][iterator]['p_barcode'] = request.POST['PBarcode' + iterator]
        context['product'][iterator]['sb_qty'] = request.POST['SBQty' + iterator]
        context['product'][iterator]['p_name'] = p_name
        context['product'][iterator]['p_price'] = p_price
        context['product'][iterator]['sb_price'] = sb_price
        iterator = str(int(iterator) + 1)

    final_price = int(total_price * (100 - c_discount_rate) // 100 // 1000 * 1000)

    context['num_products'] = int(iterator)
    context['total_price'] = int(total_price)
    context['final_price'] = int(final_price)

    print(context)
    
    request.session['context'] = context
    return HttpResponseRedirect('../sell', context)

def submit_bill(request):
    context = {
        'c_discount_rate': 0,
        'num_products': 0,
        'products': {},
        'total_price': 0,
        'final_price': 0
    }

    print(request.POST)
    customer = Customer.objects.select_related('CTier').get(pk = request.POST['CPhoneNo'])
    clerk = Clerk.objects.get(pk = request.POST['ClNo'])
    c_discount_rate = customer.CTier.DSRate

    iterator = '0'
    total_price = 0

    while ('PBarcode' + iterator) in request.POST.keys():
        product = Product.objects.get(pk = request.POST['PBarcode' + iterator])
        product.PQty -= int(request.POST['SBQty' + iterator])
        product.save()
        p_price = int(product.PPrice * (100 - product.PDiscountRate) // 100 // 1000 * 1000)
        sb_price = p_price * int(request.POST['SBQty' + iterator])
        total_price += sb_price

        iterator = str(int(iterator) + 1)

    final_price = int(total_price * (100 - c_discount_rate) // 100 // 1000 * 1000)

    sb_no = str(randint(1000000000, 9999999999))
    try:
        SellingBill.objects.get(pk = sb_no)
    except:
        selling_bill = SellingBill.objects.create(
            SBNo = sb_no,
            ClNo = clerk,
            CPhoneNo = customer,
            SBDate = datetime.now(),
            SBPrice = final_price
        )

        selling_bill.save()

        iterator = '0'
        while ('PBarcode' + iterator) in request.POST.keys():
            product = Product.objects.get(pk = request.POST['PBarcode' + iterator])
            selling_bill_detail = SellingBillDetail.objects.create(
                SBNo = selling_bill,
                PBarcode = product,
                SBQty = int(request.POST['SBQty' + iterator])
            )

            selling_bill_detail.save()
            iterator = str(int(iterator) + 1)

        customer.CPoint += int(total_price // 1000)
        customer.save()
        if customer.CPoint >= customer.CTier.DSMaxPoint:
            customer.CPoint -= customer.CTier.DSMaxPoint
            customer.save()
            if customer.CTier == DiscountService.objects.get(pk = "WOODEN"):
                customer.CTier = DiscountService.objects.get(pk = "SILVER")
            elif customer.CTier == DiscountService.objects.get(pk = "SILVER"):
                customer.CTier = DiscountService.objects.get(pk = "GOLD")
            elif customer.CTier == DiscountService.objects.get(pk = "GOLD"):
                customer.CTier = DiscountService.objects.get(pk = "DIAMOND")

        customer.save()
    else:
        pass
    finally:
        request.session['context'] = context
        return HttpResponseRedirect('../sell', context)