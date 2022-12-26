
from ntpath import join
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

STATE_CHOICES = (

    ('assam','assam'),
    ('bihar','bihar'),
    ('chandigarh','chandigarh'),
    ('gujarat','gujarat'),
    ('maharastra','maharastra'),





)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    locality= models.CharField(max_length=200)
    city= models.CharField(max_length=50)
    pincode= models.IntegerField()
    state = models.CharField(choices = STATE_CHOICES,max_length=50)

    def __str__(self) :
        return str(self.id)

CATEGORY_CHOICES =(

    ('M','mobile'),
    ('L','laptop'),
    ('TW','top wears'),
    ('BW','bottom wears'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES ,max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    
    def __str__(self) :
        return str(self.id)

class Cart(models.Model):
    user  = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    product  = models.ForeignKey(Product, on_delete= models.CASCADE,null=True, blank=True)
    quantity  = models.PositiveBigIntegerField(default=1, null=True,blank=True)


    def __str__(self) :
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price   

          


STATUS_CHOICES = (

    ('Accepted','accepted'),
    ('on the way','on the way'),
    ('delivered','delivered'),
    ('cancel','cancel'),
)

class OrderPlaced(models.Model):

    user  = models.ForeignKey(User, on_delete= models.CASCADE)
    product  = models.ForeignKey(Product, on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    quantity  = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')


