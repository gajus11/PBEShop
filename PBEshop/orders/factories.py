import factory
from decimal import Decimal

from .models import Order, OrderItem
from shop.factories import ProductFactory

class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Order

    first_name = 'first name'
    last_name = 'last name'
    email = 'fake@email.com'
    address = 'Address'
    postal_code = '90-210'
    city = 'City'

class OrderItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = Decimal(10)
    quantity = 1