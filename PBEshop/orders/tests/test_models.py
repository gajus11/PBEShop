from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from orders.factories import OrderFactory, OrderItemFactory
from orders.models import Order


class OrderTest(TestCase):
    def test_string_representation(self):
        order = OrderFactory()
        self.assertEqual(str(order), 'Order %s' % (order.id))

    def test_paid_is_False_by_default(self):
        order = OrderFactory()
        self.assertEqual(order.paid, False)

    def test_first_name_is_required(self):
        order = OrderFactory(first_name='')
        with self.assertRaises(ValidationError):
            order.save()
            order.full_clean()

    def test_last_name_is_required(self):
        order = OrderFactory(last_name='')
        with self.assertRaises(ValidationError):
            order.save()
            order.full_clean()

    def test_email_is_required(self):
        order = OrderFactory(email='')
        with self.assertRaises(ValidationError):
            order.save()
            order.full_clean()

    def test_address_is_required(self):
        order = OrderFactory(address='')
        with self.assertRaises(ValidationError):
            order.save()
            order.full_clean()

    def test_postal_code_is_required(self):
        order = OrderFactory(postal_code='')
        with self.assertRaises(ValidationError):
            order.save()
            order.full_clean()

    def test_city_code_is_required(self):
        order = OrderFactory(city='')
        with self.assertRaises(ValidationError):
            order.save()
            order.full_clean()

    def test_order_by_create(self):
        OrderFactory()
        order = OrderFactory(first_name='second_name')
        self.assertEqual(str(Order.objects.first()), 'Order %s' % (order.id))

    def test_get_total_cost(self):
        order = OrderFactory()

        order_item1 = OrderItemFactory(order=order)
        order_item2 = OrderItemFactory(order=order)

        total_cost = order_item1.get_cost() + order_item2.get_cost()
        self.assertEqual(order.get_total_cost(), total_cost)

class OrderItemTest(TestCase):

    def setUp(self):
        self.order = OrderFactory()

