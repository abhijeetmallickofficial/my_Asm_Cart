from django.db import models
from django.db.models import JSONField
from django.utils.timezone import now
import razorpay


# Create your models here.
class Product(models.Model): #product is my table name
    product_id = models.AutoField(primary_key=True) #product_id,etc are my column
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default='')
    subcategory = models.CharField(max_length=100,default='')
    price = models.FloatField(default=0)
    desc = models.CharField(max_length=320)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images',default='')

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Order(models.Model):
    items_json = models.JSONField()  # ✅ This is required
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.name}"


class OrderUpdate(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    update_desc = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Update for Order {self.order_id.id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


