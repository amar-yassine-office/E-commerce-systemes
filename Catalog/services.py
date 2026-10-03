from django.shortcuts import get_object_or_404
from .models import Category, Product, ProductAttribute, ProductImage


class CatalogService:

    # --- Categories Services ---
    @staticmethod
    def create_category(data: dict) -> Category:
        parent_id = data.pop('parent_id', None)
        parent = Category.objects.get(id=parent_id) if parent_id else None
        return Category.objects.create(parent=parent, **data)

    @staticmethod
    def get_all_categories() -> list[Category]:
        return Category.objects.filter(is_active=True)

    # --- Products Services ---
    @staticmethod
    def create_product(vendor, data: dict) -> Product:
        category_id = data.pop('category_id', None)
        attributes_data = data.pop('attributes', [])

        category = get_object_or_404(Category, id=category_id) if category_id else None

        product = Product.objects.create(vendor=vendor, category=category, **data)

        # إنشاء الخصائص المرتبطة بالمنتج
        for attr in attributes_data:
            ProductAttribute.objects.create(product=product, **attr)

        return product

    @staticmethod
    def get_all_products() -> list[Product]:
        return Product.objects.filter(is_active=True).prefetch_related('attributes', 'images')

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        return get_object_or_404(Product.objects.prefetch_related('attributes', 'images'), id=product_id)