from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path('search/', views.search, name="search"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path('products/<int:id>', views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="checkout"),
    path('proceed/', views.proceed_to_payment, name="Proceed"),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('thankyou/', views.thankyou, name="ThankYou"),  # ✅ Add this

]
