from django.shortcuts import render, HttpResponse, redirect
import requests
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Product, Order, Address
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum
import random,json,datetime
from importlib import import_module
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from account.models import Account

MERCHANT_KEY = 'J0h@C_Ac6ZhL%JiC'


# Create your views here.


def index(request):
    date = datetime.date.today()
    d=date.strftime("%x")
    print(date)
    if request.user.is_authenticated:
        profile = Account.objects.get(username=request.user)
        k = profile.date_joined.strftime("%x")
        return render(request, 'shop/index.html',{'date':d,'profile':profile,'k':k})
    else:
        return render(request, 'shop/index.html',{'date':date})


def tshirts(request):
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item["subcategory"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat)
        n = len(prod)
        allProds.append([prod, range(n), n])
    params = {'allProds': allProds}

    return render(request, 'shop/tshirts.html', params)


def hoodies(request):
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item["subcategory"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat)
        n = len(prod)
        allProds.append([prod, range(n), n])
    params = {'allProds': allProds}

    return render(request, 'shop/hoodies.html', params)


def productview(request, myid):
    prod = Product.objects.filter(id=myid)
    return render(request, 'shop/product.html', {'product': prod[0]})


def aboutus(request):
    return render(request, 'shop/aboutUs.html')





def managecart(request):
    global key
    key = request.session.session_key
    print(key)
    cartdata = {}
    cartdata[str(request.GET['id'])] = {
        'id': request.GET['id'],
        'qty': request.GET['qty'],
        'name': request.GET['name'],
        'price': int(request.GET['price']),
        'size': request.GET['size'],
        'image': request.GET['image']
    }
    if 'cart' in request.session:
        if str(request.GET['id']) in request.session['cart']:
            ca_rt = request.session['cart']
            ca_rt[str(request.GET['id'])]['qty'] = int(ca_rt[str(request.GET['id'])]['qty']) + 1
            ca_rt[str(request.GET['id'])]['size'] = ca_rt[str(request.GET['id'])]['size'] + "," + request.GET['size']
            ca_rt.update(ca_rt)
            request.session['cart'] = ca_rt
        else:
            ca_rt = request.session['cart']
            ca_rt.update(cartdata)
            request.session['cart'] = ca_rt
    else:
        request.session['cart'] = cartdata
    return JsonResponse({'data': request.session['cart']})


def cart(request):
    total = 0
    request.session.get('cart')
    if 'cart' in request.session:
        for p_id, item in request.session['cart'].items():
            total += int(item['qty']) * float(item['price'])
        return render(request, 'shop/Cart.html', {'data': request.session['cart'], 'total': total})
    else:
        return render(request, 'shop/Cart.html')


def delete_items(request):
    pid = str(request.GET['id'])
    if 'cart' in request.session:
        if pid in request.session['cart']:
            ca_rt = request.session['cart']
            del request.session['cart'][pid]
            request.session['cart'] = ca_rt
    total = 0
    for p_id, item in request.session['cart'].items():
        total += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html', {'data': request.session['cart'], 'total': total})
    return JsonResponse({'data': t})


def update_items(request):
    pid = str(request.GET['id'])
    value = request.GET['val']
    if 'cart' in request.session:
        if pid in request.session['cart']:
            ca_rt = request.session['cart']
            if value == 'minus':
                request.session['cart'][pid]['qty'] = max(0, (int(request.session['cart'][pid]['qty']) - 1))
            elif value == 'plus':
                request.session['cart'][pid]['qty'] = int(request.session['cart'][pid]['qty']) + 1
            if request.session['cart'][pid]['qty'] == 0:
                del request.session['cart'][pid]
            request.session['cart'] = ca_rt
    total = 0
    for p_id, item in request.session['cart'].items():
        total += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html', {'data': request.session['cart'], 'total': total})
    return JsonResponse({'data': t})


def checkout(request):
    if request.user.is_authenticated:
        total = 0
        request.session.get('cart')
        if 'cart' in request.session:
            for p_id, item in request.session['cart'].items():
                total += int(item['qty']) * float(item['price'])
            if request.method == "POST":
                global address
                address = Address(
                    user=request.user,
                    Hostel_name=request.POST.get('address', ''),
                    Unit=request.POST.get('unit', ''),
                    City=request.POST.get('city', ''),
                    pincode=request.POST.get('pincode', ''),
                    landmark=request.POST.get('landmark', ''),
                )
                order_id = "ORDERNO_" + str(random.randint(1,10000))
                paytmParams = dict()

                paytmParams["body"] = {
                    "requestType": "Payment",
                    "mid": "iKBIyO36141253697713",
                    "websiteName": "WEBSTAGING",
                    "orderId": order_id,
                    "callbackUrl": "http://127.0.0.1:8000/handlerequest/",
                    "txnAmount": {
                        "value": str(total),
                        "currency": "INR",
                    },
                    "userInfo": {
                        "custId": str(request.user),

                    },
                    "extendInfo":{
                        "session_key":request.session.session_key
                    },
                }

                checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)

                paytmParams["head"] = {
                    "signature": checksum
                }

                post_data = json.dumps(paytmParams)

                # for Staging
                url = f'https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=iKBIyO36141253697713&orderId={order_id}'

                # for Production
                # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
                response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()

                payment_page = {
                    'mid': 'iKBIyO36141253697713',
                    'txnToken': response['body']['txnToken'],
                    'orderId': paytmParams['body']['orderId'],
                }

                return render(request, 'shop/paytm.html', {'data': payment_page})
            return render(request, 'shop/checkout.html', {'data': request.session['cart'], 'total': total})
        else:
            return render(request, 'shop/checkout.html')
    else:
        messages.error(request, "Login required to place order")
        return redirect("/login")


@csrf_exempt
def handlerequest(request):
    engine = import_module(settings.SESSION_ENGINE)
    form = request.POST
    response_dict = {}
    global status
    status={
        "order_id" :request.POST.get('ORDERID'),
        "payment_mode ":request.POST.get('PAYMENTMODE'),
        "transaction_id" :request.POST.get('TXNID'),
        "Bank_transaction_id ": request.POST.get('BANKTXNID'),
        "transaction_date" : request.POST.get('TXNDATE'),
        "res_msg" : request.POST.get('RESPMSG'),
    }

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = PaytmChecksum.verifySignature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            address.save()
            return redirect('/success')
        else:
            return render(request, 'shop/fail.html')


def success(request):
    k = User.objects.filter(username=request.user)
    email = request.user.email
    for p_id, item in request.session['cart'].items():
        global order
        order = Order(
            user=request.user,
            items=item['name'],
            size=item['size'],
            qty=item['qty'],
            price=float(item['price']) * int(item['qty'])
        )
        order.save()
        html_content = render_to_string("shop/email.html",{'user':request.user,'prods':item,})
        text_content = strip_tags(html_content)
        mail = EmailMultiAlternatives(
            "testing",
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        mail.attach_alternative(html_content, "text/html")
        mail.send()
    del request.session['cart']
    status_details=status
    return render(request,'shop/success.html',{'response':status_details})