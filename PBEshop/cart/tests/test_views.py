from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from unittest.mock import Mock

from ..views import cart_add, cart_detail, cart_remove
from ..cart import Cart
from ..forms import CartAddProductForm
from shop.models import Product, Category

from decimal import Decimal

class CartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='category', slug='slug')
        self.product1 = Product.objects.create(category=self.category,
                                               name='product 1',
                                               slug='slug-1',
                                               description='desc',
                                               price=Decimal(1),
                                               stock=1,
                                               available=True)
        self.product2 = Product.objects.create(category=self.category,
                                               name='product 2',
                                               slug='slug-2',
                                               description='desc',
                                               price=Decimal(1),
                                               stock=1,
                                               available=True)

class CartAddTest(CartViewTest):
    def setUp(self):
        super(CartAddTest, self).setUp()

    def test_correct_redirect(self):
        response = self.client.post('/cart/add/%d/' % (self.product1.id))
        self.assertRedirects(response, '/cart/')

    def test_get_request_not_working(self):
        response = self.client.get('/cart/add/%d/' % (self.product1.id))
        self.assertEqual(response.status_code, 405)

    def test_wrong_product_id_404(self):
        response = self.client.post('/cart/add/%d/' % (self.product1.id + 2))
        self.assertEqual(response.status_code, 404)

    def test_successfull_adding(self):
        response = self.client.post('/cart/add/%d/' % (self.product1.id), {'quantity' : 1})
        response = self.client.get(response.url)
        cart = response.context[settings.CART_SESSION_ID].cart
        cart[str(self.product1.id)]

    def test_invalid_form_data(self):
        response = self.client.post('/cart/add/%d/' % (self.product1.id), {'wrong' : 1})
        response = self.client.get(response.url)
        cart = response.context[settings.CART_SESSION_ID].cart
        with self.assertRaises(KeyError):
            cart[str(self.product1.id)]


class CartRemoveTest(CartViewTest):

    def setUp(self):
        super(CartRemoveTest, self).setUp()
        self.client.post('/cart/add/%d/' % (self.product1.id), {'quantity' : 1})

    def test_correct_redirect(self):
        response = self.client.get('/cart/remove/%d/' % (self.product1.id))
        self.assertRedirects(response, '/cart/')

    def test_wrong_product_id_404(self):
        response = self.client.get('/cart/remove/%d/' % (self.product1.id + 2))
        self.assertEqual(response.status_code, 404)

    def test_successfull_remove(self):
        response = self.client.get('/cart/remove/%d/' % (self.product1.id))
        response = self.client.get(response.url)
        cart = response.context[settings.CART_SESSION_ID].cart
        with self.assertRaises(KeyError):
            cart[str(self.product1.id)]

class CartDetailTest(CartViewTest):

    def setUp(self):
        super(CartDetailTest, self).setUp()
        self.response = self.client.get('/cart/')

    def test_render_correct_template(self):
        self.assertTemplateUsed(self.response, 'cart/detail.html')

    def test_context_cart_add_update_quality_form(self):
        #Add product to cart
        self.response.context[settings.CART_SESSION_ID].add(self.product1)
        cart = self.response.context[settings.CART_SESSION_ID].cart

        #Why self.client.session[settings.CART_SESSION_ID] = cart - doesn't working?
        session = self.client.session
        session[settings.CART_SESSION_ID] = cart
        session.save()

        #Check if form is added to items
        self.response = self.client.get('/cart/')
        cart = self.response.context[settings.CART_SESSION_ID].cart
        self.assertIsInstance(cart[str(self.product1.id)]['update_quality_form'], CartAddProductForm)


    def test_context_correct_cart_data(self):
        cart = self.client.session.get(settings.CART_SESSION_ID)
        self.assertEqual(self.response.context['cart'].cart, cart)