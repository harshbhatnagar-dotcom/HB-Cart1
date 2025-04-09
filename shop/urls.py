
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="Shophome"),
    path("about/",views.aboutus,name="aboutus"),
    path("contact/",views.contactus,name="contact"),
    path("tracker/",views.track,name="tracker"),
    path("productview/<int:myid>",views.productview,name="productview"),
    path("checkout/",views.checkout,name="checkout"),
 
]
