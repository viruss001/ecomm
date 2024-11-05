from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from product.models import Product,ColorVariant,SizeVarient,Coupon
from base.emails import send_account_activation_email
# Create your models here.





class profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    profile_image=models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False,cart__user=self.user).count()
    





class Cart(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='carts')
    coupon=models.ForeignKey(Coupon,related_name="cart_coupon",on_delete=models.SET_NULL ,blank=True ,null=True)
    is_paid=models.BooleanField(default=False)
    def get_cart_totalwith(self):
        cartsitem=self.carts_item.all()
        price=[]
        for cartitem in cartsitem:
            price.append(cartitem.product.price)
            if cartitem.color_varient:
                price.append(cartitem.color_varient.price)
            if cartitem.size_varient:
                price.append(cartitem.size_varient.price)
        if self.coupon:
            if self.coupon.minimum_amount<sum(price):
                return sum(price)- self.coupon.discount_price
        return sum(price)
    def get_cart_total(self):
        cartsitem=self.carts_item.all()
        price=[]
        for cartitem in cartsitem:
            price.append(cartitem.product.price)
            if cartitem.color_varient:
                price.append(cartitem.color_varient.price
                             )
            if cartitem.size_varient:
                price.append(cartitem.size_varient.price
                             )
       
        return sum(price)
    def get_discount(self):
        if self.coupon:
            return self.coupon.discount_price




class CartItem(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='carts_item')
    product=models.ForeignKey(Product,on_delete=models.CASCADE, null=True,blank=True,related_name='products')
    color_varient=models.ForeignKey(ColorVariant,on_delete=models.CASCADE,null=True,blank=True,related_name="colorVarient")
    size_varient=models.ForeignKey(SizeVarient,on_delete=models.CASCADE,null=True,blank=True,related_name="sizeVarient")
    def get_product_price(self):
        price=[self.product.price]
        if self.color_varient:
            price.append(self.color_varient.price)
        if self.size_varient:
            price.append(self.size_varient.price)
        return sum(price)


# it is trigger when user is created then this function is trigger
@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            # instance.profile.save()
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)