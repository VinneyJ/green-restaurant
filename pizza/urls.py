#from django.conf import settings
# from .views import home

from .views import( 
                   ItemListView, 
                   ItemDetailView,
                #    about_page,
                #    contact_page,
                   add_item_to_cart,
                   remove_from_cart,   
                ) 
#from django.conf.urls.static import static
from django.urls import path, include




app_name = 'pizza'

urlpatterns = [
    # path('', views.home, name='home'),
    # path('pizza/', views.pizza_list, name='pizza_list'),
    # #Details for toppings for pizza
    # path('pizza/<int:pizza_id/', views.pizza_topping, name='pizza_topping'),
    # path('topping/', views.toppings, name='topping')
    
    path('', ItemListView.as_view(), name='home'),
    path('detail/<slug>/', ItemDetailView.as_view(), name='detail'),
    path('add_to_cart/<slug>/', add_item_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    # path('about', about_page, name='about'),
    # path('contact', views.contact_page, name='contact')
]

