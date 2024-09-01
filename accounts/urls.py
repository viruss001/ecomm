from django.urls import path
from accounts.views import login_page,regiter_page,activate_email
from accounts.views import add_to_cart,cart,remove_to_cart,remove_coupon


urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , regiter_page , name="register"),
   path('activate/<email_token>/' , activate_email , name="activate_email"), 
   path('cart/',cart,name="cart"),
   path('add_to_cart/<uid>/',add_to_cart,name='add_to_cart'),
   path('remove_to_cart/<uid>/',remove_to_cart,name='remove_to_cart'),
   path('remove_coupon/<uid>/',remove_coupon,name='remove_coupon'),

]
