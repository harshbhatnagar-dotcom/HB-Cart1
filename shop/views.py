
from django.http import HttpResponse
from django.shortcuts import render
from .models import product,contact,Orders,Orderupdate
import json

# Create your views here.
def index(request):
    products=product.objects.all()
    n=len(products)
    v={"product":products,"n":range(n)}
    return render(request,"shop/index.html",v)

def aboutus(request):
    return render(request,"shop/about.html")

def contactus(request):
    if request.method=="POST":
        name= request.POST.get("name",'')
        
        email= request.POST.get("email",'')
        phone= request.POST.get("phone",'')
        query= request.POST.get("Query",'')
        Contact=contact(name=name,email=email,phone=phone, Query=query)
        Contact.save()

    return render(request,"shop/contact.html")

def track(request):
    if request.method == "POST":
        order_id = request.POST.get("Order_id", "").strip()
        email = request.POST.get("email", "").strip()

        orders = Orders.objects.filter(Order_id=order_id, email=email)

        if orders.exists():
            order = orders.first()  # Get the actual Order object
            try:
                items = json.loads(order.items_json)  # Now this works correctly
            except Exception as e:
                items = {}
                print("Error parsing JSON:", e)

            updates = Orderupdate.objects.filter(order_id=order_id).order_by('-timestamp')

            return render(request, "shop/tracker.html", {
                "orderupdates": updates,
                "items": items
            })
        else:
            return render(request, "shop/tracker.html", {"error": "No matching order found."})

    return render(request, "shop/tracker.html")


def productview(request,myid):
    products=product.objects.filter(id=myid)
  
    return render(request, "shop/productview.html",{"product":products[0]})

def checkout(request):
    if request.method=="POST":
        item_Json=request.POST.get("itemsJson","")
        name= request.POST.get("name",'')
        amount=request.POST.get("amount","")
        email= request.POST.get("email",'')
        address=request.POST.get("address",'')
        city=request.POST.get("city",'')
        state=request.POST.get("state",'')
        zip_code=request.POST.get("zip",'')
        phone= request.POST.get("phone",'')
        
        checkout=Orders(name=name,email=email,phone=phone, address=address,city=city,state=state,zip_code=zip_code, items_json=item_Json,amount=amount)
        checkout.save()
        update=Orderupdate(order_id=checkout.Order_id,update_desc="order has been placed")
        update.save()
        thank=True
        id=checkout.Order_id
        return render(request,"shop/checkout.html",{"thank":thank,"id":id})
    return render(request,"shop/checkout.html")

