from decimal import Decimal

from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from unittest.mock import Mock

from ..cart import Cart

from shop.factories import CategoryFactory, ProductFactory

from django.contrib.auth import get_user_model
User = get_user_model()

class CartTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = Mock()
        self.request.session = self.client.session
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)

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

    def test_remove_element_exist(self):
        cart = Cart(self.request)
        cart.add(self.product)
        cart.remove(self.product)
        self.assertEqual(cart.cart, {})

    def test_remove_element_not_exist(self):
        cart = Cart(self.request)
        cart.add(self.product)
        product = ProductFactory(category=self.category)
        cart.remove(product)
        self.assertNotEqual(cart.cart, {})
        with self.assertRaises(KeyError):
            cart.cart[str(product.id)]


    def test_clear(self):
        cart = Cart(self.request)
        cart.add(self.product)
        cart.clear()
        with self.assertRaises(KeyError):
            self.request.session[settings.CART_SESSION_ID]

    def test_get_total_price(self):
        product = ProductFactory(category=self.category)
        cart = Cart(self.request)
        cart.add(self.product)
        cart.add(product, quantity=2)
        total_price = self.product.price + product.price*2
        self.assertEqual(cart.get_total_price(), Decimal(total_price))

    def test_iteration(self):
        product = ProductFactory(category=self.category)
        cart = Cart(self.request)
        cart.add(self.product)
        cart.add(product, quantity=2)

        i = 0

        for prod in cart:
            if prod['product'] == self.product:
                self.assertEqual(prod['price'], self.product.price)
            elif prod['product'] == product:
                self.assertEqual(prod['price'], product.price)
            else:
                self.fail()
            i += 1

        self.assertEqual(i, 2)

    def test_len(self):
        product = ProductFactory(category=self.category)
        cart = Cart(self.request)
        cart.add(self.product)
        cart.add(product, quantity=2)
        self.assertEqual(cart.__len__(), 3)
