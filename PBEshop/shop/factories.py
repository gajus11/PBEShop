import factory
from decimal import Decimal

from django.template.defaultfilters import slugify

from .models import Product, Category

class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Category %d' % (n))
    slug = factory.LazyAttribute(lambda a: slugify(a.name))

class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(lambda n: 'Product %d' % (n))
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    description = factory.LazyAttribute(lambda a: 'Description %s' % (a.slug))
    price = factory.Sequence(lambda n: Decimal(n))
    stock = factory.Sequence(lambda n: n+1)