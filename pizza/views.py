from django.shortcuts import render
from .models import Item, OrderItem, Order

# Create your views here.

# def home(request):
#     return render(request, 'pizza/home.html')

# def pizza_list(request):
#     pizza = Pizza.objects.order_by('-date_added')
#     context = {'pizzas':pizza}
#     return render(request, 'pizza/pizza.html', context)

# def toppings(request):
#     topping = Topping.objects.order_by('-date_added')
#     context = {'toppings':topping}
#     return render(request, 'pizza/topping.html', context)

# def pizza_topping(request, pizza_id):
#     pizz = Pizza.objects.get(id=pizza_id)
#     topp = pizz.topping_set.order_by('-date_added')
#     context = {'pizza':pizz, 'topping':topp}
#     return render(request, 'pizza/pizza_detail.html', context)

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'pizza/items.html', context)

