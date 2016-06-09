from django.test import TestCase

from decimal import Decimal

from ..views import product_list
from ..models import Category, Product
from ..factories import CategoryFactory, ProductFactory

class ProductListTest(TestCase):

    def setUp(self):
        #create categories
        self.category1 = CategoryFactory()
        self.category2 = CategoryFactory()

        #create products
        self.product1 = ProductFactory(category=self.category1)
        self.product2 = ProductFactory(category=self.category1)
        self.product3 = ProductFactory(category=self.category2)
        self.product4 = ProductFactory(category=self.category2,
                                       available=False)

    def test_render_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'shop/product/list.html')

        response = self.client.get('/%s/' % (self.category1.slug))
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_context_category_empty_for_default(self):
        response = self.client.get('/')
        self.assertEqual(response.context['category'], None)

    def test_context_category_correct_for_slug(self):
        response = self.client.get('/%s/' % (self.category1.slug))
        self.assertEqual(response.context['category'], self.category1)

    def test_context_category_404_for_wrong_slug(self):
        response = self.client.get('/third-category/')
        self.assertEqual(response.status_code, 404)

    def test_context_categories_show_all(self):
        response = self.client.get('/')
        categories = response.context['categories']
        self.assertEqual(len(categories), 2)

    def test_context_products_show_available(self):
        response = self.client.get('/')
        products = response.context['products']
        self.assertEqual(len(products), 3)

    def test_context_product_show_in_category(self):
        response = self.client.get('/%s/' % (self.category1.slug))
        products = response.context['products']
        self.assertEqual(len(products), 2)

class ProductDetailTest(TestCase):

    def setUp(self):
        category = Category(name='first category', slug='first-category')
        category.save()

        Product.objects.create(category=category,
                               name='first',
                               slug='first',
                               price=Decimal(1),
                               stock=1,
                               available=True)

    def test_render_correct_template(self):
        product = Product.objects.first()
        product_url = '/%d/%s/' % (product.id, product.slug)
        response = self.client.get(product_url)
        self.assertTemplateUsed(response, 'shop/product/detail.html')

    def test_context_product_show_by_slug_and_id(self):
        product = Product.objects.first()
        product_url = '/%d/%s/' % (product.id, product.slug)
        response = self.client.get(product_url)
        self.assertEqual(response.context['product'], product)

    def test_context_product_404(self):
        response = self.client.get('/0/bad-slug/')
        self.assertEqual(response.status_code, 404)
