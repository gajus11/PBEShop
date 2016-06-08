from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from decimal import Decimal

from ..models import Category, Product
from ..factories import CategoryFactory, ProductFactory

class CategoryModelTest(TestCase):

    def test_get_absolute_url(self):
        CategoryFactory()
        category = Category.objects.first()
        self.assertEqual(category.get_absolute_url(), '/%s/' % (category.slug))


    def test_string_representation(self):
        category = CategoryFactory()
        self.assertEqual(str(category), category.name)

    def test_name_is_required(self):
        category = CategoryFactory(name='')
        with self.assertRaises(ValidationError):
            category.save()
            category.full_clean()

    def test_slug_is_required(self):
        category = CategoryFactory(slug='')
        with self.assertRaises(ValidationError):
            category.save()
            category.full_clean()

    def test_save_correct_category(self):
        category = CategoryFactory()
        category.save()
        category.full_clean()

    def test_slug_is_unique(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory.build(slug=category1.slug)
        with self.assertRaises(IntegrityError):
            category2.save()

    def test_ordering_by_name(self):
        CategoryFactory(name='b')
        CategoryFactory(name='a')
        self.assertEqual(str(Category.objects.first()), 'a')

class ProductModelTest(TestCase):

    def test_get_absolute_url(self):
        category = CategoryFactory()
        product = ProductFactory(category=category)
        self.assertEqual(product.get_absolute_url(), '/%d/%s/' % (product.id, product.slug))

    def test_save_correct_product(self):
        product = ProductFactory()
        product.full_clean()

    def test_category_is_required(self):
        product = Product(name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(1),
                          stock=1,
                          available=True)
        with self.assertRaises(IntegrityError):
            product.save()
            product.full_clean()

    def test_name_is_required(self):
        category = CategoryFactory()
        product = ProductFactory.build(name='',
                                       category=category)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_slug_is_required(self):
        category = CategoryFactory()
        product = ProductFactory.build(slug='',
                                       category=category)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_description_is_optional(self):
        category = CategoryFactory()
        product = ProductFactory.build(description='',
                                       category=category)

        product.save()
        product.full_clean()

    def test_price_is_required(self):
        category = CategoryFactory()
        product = ProductFactory.build(price=None,
                                       category=category)
        with self.assertRaises(IntegrityError):
            product.save()
            product.full_clean()

    def test_stock_is_required(self):
        category = CategoryFactory()
        product = ProductFactory.build(stock=None,
                                       category=category)
        with self.assertRaises(IntegrityError):
            product.save()
            product.full_clean()

    def test_price_cannot_be_negative(self):
        category = CategoryFactory()
        product = ProductFactory.build(price=Decimal(-1),
                                       category=category)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_price_can_be_zero(self):
        category = CategoryFactory()
        product = ProductFactory.build(price=Decimal(0),
                                       category=category)
        product.save()
        product.full_clean()

    def test_stock_must_be_ge_zero(self):
        category = CategoryFactory()
        product = ProductFactory.build(stock=-1,
                                       category=category)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_available_dafault_is_True(self):
        product = ProductFactory()
        self.assertEqual(product.available, True)

    def test_ordering(self):
        ProductFactory(name='b')
        ProductFactory(name='a')

        self.assertEqual(str(Product.objects.first()), 'a')

    def test_string_representation(self):
        product = ProductFactory()
        self.assertEqual(str(product), product.name)

