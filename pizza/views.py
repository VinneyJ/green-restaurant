from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order

# Create your views here.

# def home(request):
#     return render(request, 'home.html')

# def pizza_list(request):
#     pizza = Pizza.objects.order_by('-date_added')
#     context = {'pizzas':pizza}
#     return render(request, 'pizza/home.html', context)

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
    paginate_by = 8
    template_name = 'home.html'
    
    

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'
    
    # def detail_page(request):
    #     return render(request, 'detail.html')

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
            messages.success(request, "The item quantity has been updated to the cart")
            return redirect("pizza:detail", slug=slug) 
        else:
            order.items.add(order_item)
            messages.success(request, "The item has been added to the cart")
            return redirect("pizza:detail", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request,"The item has bee added to the cart")  
        return redirect("pizza:detail", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        
        if order.items.filter(item__slug=slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, 
                user=request.user, 
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.success(request,"The item has been removed from the cart")
            return redirect("pizza:detail", slug=slug)
        else:
            #message the Item does not exist
            messages.success(request,"The item was not in your cart")
            return redirect("pizza:detail", slug=slug)
        
    else:
        messages.success(request,"You do not have an active order")
        return redirect("pizza:detail", slug=slug)