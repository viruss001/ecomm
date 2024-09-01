from django.contrib import admin
from .models import Category,ProductImg,Product,ColorVariant,SizeVarient,Coupon
# Register your models here.
admin.site.register(Category)
class ProductImageAdmin(admin.StackedInline):
    model =ProductImg

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name' , 'price']
    model = ColorVariant

@admin.register(SizeVarient)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name' , 'price']

    model = SizeVarient
admin.site.register(ProductImg)
admin.site.register(Coupon)
admin.site.register(Product,ProductAdmin)