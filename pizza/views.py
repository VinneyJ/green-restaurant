from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .forms import CheckOutForm
from django.utils import timezone
from .models import Item, OrderItem, Order, BillingAddress, Payment

import stripe
stripe.api_key = "sk_test_cqQW4am9ma3f3Dcy9CeRc9NS00RfhAqdoM"

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token


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
    
    
class OrderSummaryView(LoginRequiredMixin, View):
    
    def get(self, *args, **kwargs):
        try:   
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('/')
        

def about_page(request):
    return render(request, 'about.html')



class CheckoutView(View):
    def get(self, *args, **kwargs):
        #form
        form = CheckOutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout-page.html', context)
    
    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address =form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                
                #TODO: addfunctionality for these fields
                # same_shipping_address = form.cleaned_data.get('same_shiping_address')
                # save_info = form.cleaned_data.get('save_info')
                
                payment_option = form.cleaned_data.get('payment_option')
                
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip,
                    
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                
                #TODO: add a redirect to the selected payment option
                return redirect('pizza:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('pizza:checkout')
        
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('pizza:order-summary')

        form = CheckOutForm(self.request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            print("The form is valid")
            return redirect('pizza:checkout')
        messages.warning(self.request, "Failed checkout")
        return redirect('pizza:checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        return render(self.request, 'payment.html')
    
    def post(self, *args, **kwargs):
        
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_items_price() * 100)
        
        try:
            charge = stripe.Charge.create(
                amount= amount,
                currency="usd",
                source= token,
            )
            #Create payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_items_price()
            payment.save()

            order.ordered = True
            order.payment = payment
            order.save()

            message.success(self.request, "Your order was successful!")
            return redirect('/')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            messages.error(self.request, f"{(err.get('message'))}")
            return redirect('/')
        
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.error(self.request, "Rate Limit Error")
            return redirect('/')
    
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Parameters Error")
            return redirect('/')
    
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication Error")
            return redirect('/')
    
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect('/')
    
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.error(self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect('/')
    
        except Exception as e:
        # Something else happened, completely unrelated to Stripe
        # Send an email to myself
            messages.error(self.request, "A serious error. We have been notified.")
            return redirect('/')
        
        


def contact_page(request):
    return render(request, 'contact.html')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'
    

    
    # def detail_page(request):
    #     return render(request, 'detail.html')
    
    
@login_required
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
            return redirect("pizza:order-summary") 
        else:
            order.items.add(order_item)
            messages.success(request, "The item has been added to the cart")
            return redirect("pizza:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request,"The item has been added to the cart")  
        return redirect("pizza:detail")

@login_required
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
            return redirect("pizza:order-summary")
        else:
            #message the Item does not exist
            messages.success(request,"The item was not in your cart")
            return redirect("pizza:detail", slug=slug)
        
    else:
        messages.success(request,"You do not have an active order")
        return redirect("pizza:detail", slug=slug)
    
@login_required
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.success(request,"Your Cart has been updated")
            return redirect("pizza:order-summary")
        else:
            #message the Item does not exist
            messages.success(request,"The item was not in your cart")
            return redirect("pizza:detail")
        
    else:
        messages.success(request,"You do not have an active order")
        return redirect("pizza:detail")