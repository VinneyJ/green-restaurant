from django.conf import settings
from django.db import models
from django.shortcuts import reverse

# Create your models here.
CATEGORY_CHOICES = (
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
    title = models.CharField(max_length=30)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField()
    overview = models.CharField(max_legth=20)
    description = models.TextField()
    
    
    #image = models.ImageField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return self.title
   
    def get_absolute_url(self):
       return reverse("pizza:detail", kwargs={
           'slug': self.slug
       })
       
    def get_add_to_cart_url(self):
        return reverse("pizza:add_to_cart", kwargs={
           'slug': self.slug
       })
        
    def get_remove_from_cart_url(self):
        return reverse("pizza:remove_from_cart", kwargs={
           'slug': self.slug
       })
        



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    
    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

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