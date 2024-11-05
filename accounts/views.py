from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from .models import profile
from accounts.models import Cart,CartItem
from product.models import Product,SizeVarient,Coupon
# Create your views here.
def login_page(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, 'Account not Found')
            return HttpResponseRedirect(request.path_info)
        if not user_obj[0].profile.is_email_verified:#using releted name
            messages.warning(request, 'your account is not verified ')
            return HttpResponseRedirect(request.path_info)
        user_obj=authenticate(username=email,password=password)
        if user_obj:
            login(request,user_obj)
            return HttpResponseRedirect ('/')
        messages.warning(request,"Invalid Username or Password")
        return HttpResponseRedirect(request.path_info)
    

    return render(request,"accounts/login.html")



def regiter_page(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        user_obj=User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)#redierct on same page
    return render(request,"accounts/register.html")

def activate_email(request , email_token):
    try:
        user = profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token'+str(e))
    
def cart(request):
    try:
        cart=Cart.objects.get(is_paid=False,user=request.user)
        price=cart.get_cart_total()
        cartsitem=CartItem.objects.filter(cart=cart)
        if request.method=="POST":
            coupon=request.POST.get("coupon")
            coupon_obj=Coupon.objects.filter(coupon_code=coupon)
            if not coupon_obj.exists():
                messages.warning(request,"Invalid coupon code")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart.coupon:
                messages.warning(request,"you already use this coupon")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            

            if cart.get_cart_total()<coupon_obj[0].minimum_amount:
                print(cart.get_cart_total())
                messages.warning(request,f"Amount shoud be greater then {coupon_obj[0].minimum_amount}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if coupon_obj[0].is_expired:
                messages.warning(request,"Coupon is expired ")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            cart.coupon=coupon_obj[0]
            cart.save()
            messages.success(request,"coupon is applied")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context={'carts':cart,'cartsitem':cartsitem[::-1],"price":price}
        return render(request,"accounts/Carts.html",context)
    except Exception as e :
        print("something wrong in cart" + str(e))
    return render(request,"accounts/Carts.html")

def add_to_cart(request,uid):
    variant=request.GET.get('variant')
    product=Product.objects.get(uid=uid)
    user=request.user
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item=CartItem.objects.create(cart=cart,product=product,)
    if variant:
        variant=request.GET.get('variant')
        size_var=SizeVarient.objects.get(size_name=variant)
        # print(size_var)
        cart_item.size_varient=size_var
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def remove_to_cart(request,uid):
    try:
        
        
        cart=CartItem.objects.get(uid=uid)
        cart.delete()
    except  Exception as e:
        print(e)
        return HttpResponse("something went wrong")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_coupon(request,uid):
    cart=Cart.objects.get(uid=uid)
    cart.coupon=None
    cart.save()
    messages.success(request,"coupon is removed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# admin admin pass
