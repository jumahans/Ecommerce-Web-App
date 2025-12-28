from django.db import models
import string
import random
from django.utils import timezone
from django.contrib.auth.models import User

def unique_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=20))

# Product category  
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image')
    slug = models.SlugField(unique=True)

    def __str__ (self):
        return self.title
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['title']

# Products
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='published')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='image')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, default='No description provided')
    date = models.DateField(default=timezone.now)

    def __str__ (self):
        return self.name
    
    class Meta:
        verbose_name_plural = "products"

class Variant(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    def __str__ (self):
        return self.name
    
class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, null=True, on_delete=models.SET_NULL)
    title = models.CharField(verbose_name="Item Title" ,max_length=1000)
    content = models.CharField(verbose_name="Item Content", max_length=1000)

    def __str__ (self):
        return self.title
    
class Coupon(models.Model):
    vendor = models.ForeignKey("auth.user", on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(default=1)

    def __str__ (self):
        return self.code

class Order(models.Model):
    # User Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ManyToManyField('auth.User', blank=True, related_name='orders')
    customer = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL, related_name='customer_orders')
    
    # Order Information
    order_id = models.CharField(unique=True, default=unique_id, max_length=100)
    payment_status = models.CharField(max_length=100, default="Processing")
    payment_method = models.CharField(max_length=100, default="None")
    order_status = models.CharField(max_length=100, default="Processing")
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    payment_id = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # ✅ NEW SHIPPING INFORMATION FIELDS
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-date']  # Changed to show newest first

    def __str__ (self):
        return self.order_id
    
    def order_items(self):
        return OrderItem.objects.filter(order=self)
    
    def get_total(self):
        """Calculate total from order items"""
        return sum(item.price * item.quantity for item in self.order_items())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    order_status = models.CharField(default='Pending', max_length=100)
    shipping_services = models.CharField(max_length=100, default='None')
    tracking_id = models.CharField(max_length=100, unique=True, default=unique_id)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='vendor_orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_products = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.tracking_id
    
    def get_total(self):
        """Calculate total for this order item"""
        return self.price * self.quantity

RATTING = (
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★')
)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    reply = models.TextField(null=True, blank=True)
    ratting = models.IntegerField(choices=RATTING)

    def __str__ (self):
        return f"Review by {self.user.username if self.user else 'Unknown'} on {self.product.name if self.product else 'Unknown'}"

class Gallery(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    image = models.FileField(verbose_name='image', default='gallery.jpg')
    content = models.CharField(unique=True, max_length=100, default=unique_id)

    def __str__ (self):
        return f"Gallery for {self.product.name if self.product else 'Unknown'}"

class MyCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    total_products = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    cart_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_products = self.quantity
        super(MyCart, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.cart_id} - {self.product.name if self.product else "No Product"}'
    
    def get_total(self):
        """Calculate total for this cart item"""
        return self.price * self.quantity


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='user_images/', null=True, blank=True, default='user_images/default.jpg')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"