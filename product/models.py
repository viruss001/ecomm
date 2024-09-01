from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.
class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category_image=models.ImageField(upload_to="category")


    def save(self,*args,**kwags):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwags)
    def __str__(self) -> str:
        return self.category_name
    
class ColorVariant(BaseModel):
    color_name=models.CharField(max_length=100)
    price= models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.color_name
class SizeVarient(BaseModel):
    size_name=models.CharField(max_length=100)
    price= models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.size_name

class Product(BaseModel):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category=models.ForeignKey(Category,related_name="category",on_delete=models.CASCADE)
    price =models.IntegerField()
    product_desc=models.TextField()
    color_variant=models.ManyToManyField(ColorVariant)
    size_variant=models.ManyToManyField(SizeVarient)
    
    
    
    def save(self,*args,**kwags):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args,**kwags)
    def __str__(self) -> str:
        return self.product_name
    def get_product_price_by_size(self,size):
        return self.price+SizeVarient.objects.get(size_name=size).price

class ProductImg(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_image")
    img=models.ImageField(upload_to="product_img")
    def __str__(self) -> str:
        return self.product.product_name+" "
    
class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=10)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=500)
    def __str__(self):
        return self. coupon_code