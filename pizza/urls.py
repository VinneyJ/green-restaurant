#from django.conf import settings
from .views import item_list
#from django.conf.urls.static import static
from django.urls import path, include


from . import views

app_name = 'pizza'

urlpatterns = [
    # path('', views.home, name='home'),
    # path('pizza/', views.pizza_list, name='pizza_list'),
    # #Details for toppings for pizza
    # path('pizza/<int:pizza_id/', views.pizza_topping, name='pizza_topping'),
    # path('topping/', views.toppings, name='topping')
    
    path('', item_list, name='item-list')
]

