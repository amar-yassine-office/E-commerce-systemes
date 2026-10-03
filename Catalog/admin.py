from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    list_editable = ('is_active', 'parent')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'vendor', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description', 'vendor__username', 'vendor__email')
    list_editable = ('price', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ProductAttributeInline]

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'slug', 'vendor', 'category', 'description')
        }),
        ('التسعير', {
            'fields': ('price', 'compare_at_price')
        }),
        ('الحالة والظهور', {
            'fields': ('is_active',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )