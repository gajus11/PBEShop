from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from decimal import Decimal

from ..models import Category, Product

class CategoryModelTest(TestCase):

    def test_get_absolute_url(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        self.assertEqual(category.get_absolute_url(), '/%s/' % (category.slug))


    def test_string_representation(self):
        category = Category(name='name', slug='slug')
        self.assertEqual(str(category), 'name')

    def test_name_is_required(self):
        category = Category(slug='slug')
        with self.assertRaises(ValidationError):
            category.save()
            category.full_clean()

    def test_slug_is_required(self):
        category = Category(name='name')
        with self.assertRaises(ValidationError):
            category.save()
            category.full_clean()

    def test_save_correct_category(self):
        category = Category(name='name', slug='slug')
        category.save()
        category.full_clean()

    def test_slug_is_unique(self):
        Category.objects.create(name='name', slug='slug')
        category = Category(name='name2', slug='slug')
        with self.assertRaises(IntegrityError):
            category.save()

    def test_ordering_by_name(self):
        Category.objects.create(name='b', slug='b')
        Category.objects.create(name='a', slug='a')
        self.assertEqual(str(Category.objects.first()), 'a')

class ProductModelTest(TestCase):

    def test_get_absolute_url(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product.objects.create(category=category,
                                         name='name',
                                         slug='slug',
                                         description='desc',
                                         price=Decimal(1),
                                         stock=1,
                                         available=True)
        self.assertEqual(product.get_absolute_url(), '/%d/%s/' % (product.id, product.slug))

    def test_save_correct_product(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(1),
                          stock=1,
                          available=True)
        product.save()
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
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          slug='slug',
                          description='desc',
                          price=Decimal(1),
                          stock=1,
                          available=True)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_slug_is_required(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          description='desc',
                          price=Decimal(1),
                          stock=1,
                          available=True)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_description_is_optional(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          price=Decimal(1),
                          stock=1,
                          available=True)

        product.save()
        product.full_clean()

    def test_price_is_required(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          stock=1,
                          available=True)
        with self.assertRaises(IntegrityError):
            product.save()
            product.full_clean()

    def test_stock_is_required(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(1),
                          available=True)
        with self.assertRaises(IntegrityError):
            product.save()
            product.full_clean()

    def test_price_cannot_be_negative(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(-1),
                          stock=1,
                          available=True)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_price_can_be_zero(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(0),
                          stock=1,
                          available=True)
        product.save()
        product.full_clean()

    def test_stock_must_be_positive(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(1),
                          stock=-1,
                          available=True)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_available_dafault_is_True(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(1),
                          stock=1)
        self.assertEqual(product.available, True)

    def test_ordering(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()

        Product.objects.create(category=category,
                          name='a',
                          slug='slug',
                          description='desc',
                          price=Decimal(-1),
                          stock=0,
                          available=True)

        Product.objects.create(category=category,
                          name='b',
                          slug='slug',
                          description='desc',
                          price=Decimal(-1),
                          stock=0,
                          available=True)

        self.assertEqual(str(Product.objects.first()), 'a')

    def test_string_representation(self):
        Category.objects.create(name='name', slug='slug')
        category = Category.objects.first()
        product = Product(category=category,
                          name='name',
                          slug='slug',
                          description='desc',
                          price=Decimal(-1),
                          stock=0,
                          available=True)
        self.assertEqual(str(product), 'name')

