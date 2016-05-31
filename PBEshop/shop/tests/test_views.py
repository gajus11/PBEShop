from django.test import TestCase

from decimal import Decimal

from ..views import product_list
from ..models import Category, Product

class ProductListTest(TestCase):

    def setUp(self):
        #create categories
        category1 = Category(name='first category', slug='first-category')
        category1.save()
        category2 = Category(name='second category', slug='second-category')
        category2.save()

        #create products
        Product.objects.create(category=category1,
                               name='first',
                               slug='first',
                               price=Decimal(1),
                               stock=1,
                               available=True)
        Product.objects.create(category=category1,
                               name='second',
                               slug='second',
                               price=Decimal(1),
                               stock=1,
                               available=True)
        Product.objects.create(category=category2,
                               name='third',
                               slug='third',
                               price=Decimal(1),
                               stock=1,
                               available=True)
        Product.objects.create(category=category2,
                               name='fourth',
                               slug='fourth',
                               price=Decimal(1),
                               stock=1,
                               available=False)

    def test_render_correct_template(self):
        pass

    def test_context_category_empty_for_default(self):
        # response = self.client.get('')
        pass

    def test_context_category_correct_for_slug(self):
        pass

    def test_context_category_404_for_wrong_slug(self):
        pass

    def test_context_categories_show_all(self):
        pass

    def test_context_products_show_available(self):
        pass