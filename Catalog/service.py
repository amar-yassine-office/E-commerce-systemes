from django.utils.text import slugify
from .models import Category, Product, ProductImage, ProductAttribute
from .tasks import optimize_product_image_task, notify_vendor_product_status_task


class CatalogService:

    @staticmethod
    def create_product(vendor, category, title, description, price, compare_at_price=None, is_active=True):
        """
        Creates a new product, generates a unique slug, and triggers a background notification task.
        """
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        # Ensure unique slug generation
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product = Product.objects.create(
            vendor=vendor,
            category=category,
            title=title,
            slug=slug,
            description=description,
            price=price,
            compare_at_price=compare_at_price,
            is_active=is_active
        )

        # Trigger background celery task to notify the vendor
        notify_vendor_product_status_task.delay(product.id)
        return product

    @staticmethod
    def add_product_image(product, image_file, is_feature=False):
        """
        Adds an image to a product and triggers a background optimization task.
        """
        product_image = ProductImage.objects.create(
            product=product,
            image=image_file,
            is_feature=is_feature
        )

        # Trigger background image processing task
        optimize_product_image_task.delay(product_image.id)
        return product_image

    # the cache function for delete the data that macke update

    from django.utils.text import slugify
    from cache import RedisCacheManager
    from .models import Category, Product, ProductImage, ProductAttribute
    from .tasks import optimize_product_image_task, notify_vendor_product_status_task

    class CatalogService:

        @staticmethod
        def get_all_categories():
            categories = RedisCacheManager.get_catalog_categories()

            if categories is not None:
                return categories

            categories = list(Category.objects.filter(is_active=True).values('id', 'name', 'slug', 'parent_id'))

            RedisCacheManager.set_catalog_categories(categories, timeout=60 * 30)
            return categories

        @staticmethod
        def create_category(name, parent=None, is_active=True):
            base_slug = slugify(name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            category = Category.objects.create(
                name=name,
                slug=slug,
                parent=parent,
                is_active=is_active
            )

            RedisCacheManager.clear_catalog_categories()
            return category

        @staticmethod
        def create_product(vendor, category, title, description, price, compare_at_price=None, is_active=True):
            base_slug = slugify(title)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            product = Product.objects.create(
                vendor=vendor,
                category=category,
                title=title,
                slug=slug,
                description=description,
                price=price,
                compare_at_price=compare_at_price,
                is_active=is_active
            )

            notify_vendor_product_status_task.delay(product.id)
            return product

        @staticmethod
        def add_product_image(product, image_file, is_feature=False):
            product_image = ProductImage.objects.create(
                product=product,
                image=image_file,
                is_feature=is_feature
            )

            RedisCacheManager.clear_catalog_product(product.slug)
            optimize_product_image_task.delay(product_image.id)
            return product_image