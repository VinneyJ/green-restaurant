from django.conf import settings
from django.db import models

# Create your models here.
TAKEOUT_TYPE = (
    ('food', 'Food'),
    ('dri', 'Drinks'),
    ('bev', 'Beverage'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=20)
    price = models.FloatField()
    #discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=TAKEOUT_TYPE, max_length=5)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    #slug = models.SlugField()
    #description = models.TextField()
    #image = models.ImageField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return self.title
    
    
# class Pizza_Type(models.Model):
#     pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
#     pizza_type = models.CharField(choices=PIZZA_TYPES, max_length=10)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.pizza_type
    
    
# class Topping(models.Model):
#     pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
#     topping_name = models.CharField(max_length=30)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         verbose_name_plural = 'toppings'
        
#     def __str__(self):
#         return self.topping_name



class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.item

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user
    