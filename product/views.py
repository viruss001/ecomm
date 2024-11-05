from django.shortcuts import render
from product.models import Product

# Create your views here.
def get_product(request , slug):
    # print(request.user.profile.get_cart_count)
    try:
        product = Product.objects.get(slug =slug)
        context = {'product' : product}
        if request.GET.get('size'):
            size=request.GET.get('size')
            price=product.get_product_price_by_size(size)
            context['select_size']=size
            context['updated_price']=price
            print(context)
        return render(request  , 'product/product.html' ,context)

    except Exception as e:
        print(e)
    return render(request  , 'product/product.html' )
