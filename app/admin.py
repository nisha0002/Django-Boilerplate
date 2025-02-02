

# Register your models here.
from django.contrib import admin
from .models import (Customer, Product,OrderPlaced,Cart)

# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','pincode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity','customer','ordered_date','status']







