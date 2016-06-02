from decimal import Decimal

from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from unittest.mock import Mock

from ..cart import Cart

from shop.models import Product, Category

from django.contrib.auth import get_user_model
User = get_user_model()

class CartTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = Mock()
        self.request.session = self.client.session
        self.category = Category.objects.create(name='category', slug='slug')
        self.product = Product.objects.create(category=self.category,
                               name='name',
                               slug='slug',
                               description='desc',
                               price=Decimal(1),
                               stock=1,
                               available=True)

    def test_initialization(self):
        cart = Cart(self.request)
        self.assertEqual(cart.cart, {})

    def test_add_new_product(self):
        cart = Cart(self.request)
        cart.add(self.product)
        self.assertEqual(cart.cart[str(self.product.id)]['quantity'], 1)

    def test_add_update_quantity(self):
        cart = Cart(self.request)
        cart.add(self.product)
        cart.add(self.product, quantity=2, update_quantity=True)
        self.assertEqual(cart.cart[str(self.product.id)]['quantity'], 2)

    def test_add_quality_of_product(self):
        cart = Cart(self.request)
        cart.add(self.product)
        cart.add(self.product, quantity=2, update_quantity=False)
        self.assertEqual(cart.cart[str(self.product.id)]['quantity'], 3)

    def test_remove(self):
        cart = Cart(self.request)
        cart.add(self.product)
        cart.remove(self.product)
        self.assertEqual(cart.cart, {})

    def test_clear(self):
        cart = Cart(self.request)
        cart.add(self.product)
        cart.clear()
        with self.assertRaises(KeyError):
            self.request.session[settings.CART_SESSION_ID]

    def test_get_total_price(self):
        product = Product.objects.create(category=self.category,
                                         name='name',
                                         slug='slug',
                                         description='desc',
                                         price=Decimal(2),
                                         stock=2,
                                         available=True)
        cart = Cart(self.request)
        cart.add(self.product)
        cart.add(product, quantity=2)
        total_price = self.product.price + product.price*2
        self.assertEqual(cart.get_total_price(), Decimal(total_price))
