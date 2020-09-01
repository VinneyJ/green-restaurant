from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
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



class ItemListView(ListView):
    model = Item
    template_name = 'index.html'
    
    

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'
    
def detail_page(request):
    return render(request, 'detail.html')

def add_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, 
        user=request.user, 
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #Check if the order Exists
        if order.items.filter(item__slug=slug).exists():
            order_item.quantity += 1
            order_item.save() 
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("pizza:detail", slug=slug)