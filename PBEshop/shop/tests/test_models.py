from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ..models import Category, Product

class CategoryModelTest(TestCase):

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