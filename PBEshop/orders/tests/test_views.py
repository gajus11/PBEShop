from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from ..forms import OrderCreateForm
from ..factories import OrderFactory, OrderItemFactory
from shop.factories import CategoryFactory, ProductFactory

class OrderCreateTest(TestCase):

    def setUp(self):
        # Add products to cart
        self.client = Client()
        quantity_dict = {'quantity': 1}
        self.product1 = ProductFactory()
        self.client.post('/cart/add/%d/' % (self.product1.id), quantity_dict)
        self.product2 = ProductFactory()
        self.client.post('/cart/add/%d/' % (self.product2.id), quantity_dict)
        self.product3 = ProductFactory()
        self.client.post('/cart/add/%d/' % (self.product3.id), quantity_dict)
        self.order = OrderFactory()
        self.order_form_dict = {
            'first_name' : self.order.first_name,
            'last_name' : self.order.last_name,
            'email' : self.order.email,
            'address' : self.order.address,
            'postal_code' : self.order.postal_code,
            'city' : self.order.city,
        }

    def test_render_correct_template_on_GET(self):
        response = self.client.get('/orders/create/')
        self.assertTemplateUsed(response, 'orders/order/create.html')

    def test_render_correct_template_on_POST(self):
        response = self.client.post('/orders/create/', self.order_form_dict)
        self.assertTemplateUsed(response, 'orders/order/created.html')

    def test_render_correct_template_if_form_invalid(self):
        order_form_dict = self.order_form_dict
        order_form_dict['first_name'] = ''
        response = self.client.post('/orders/create/', order_form_dict)
        self.assertTemplateUsed(response, 'orders/order/create.html')

    def test_context_on_POST(self):
        response = self.client.post('/orders/create/', self.order_form_dict)
        order = response.context['order']
        self.assertEqual(order.items.count(), 3)

    def test_context_form_on_GET(self):
        response = self.client.get('/orders/create/')
        form = response.context['form']
        self.assertIsInstance(form, OrderCreateForm)

    def test_context_cart_on_GET(self):
        response = self.client.get('/orders/create/')
        cart = response.context['cart']
        self.assertEqual(len(cart.cart), 3)