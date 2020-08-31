from django.test import TestCase
from django.urls import reverse

from ..models import Order, OrderDetail, User, Product, Category, Customer

DEFAULT_AVATAR = 'media/profile_pics/default.jpg'


class OrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Drinks')
        Product.objects.create(name='milk tea', category_id=1, price=23.00, quantity=10, vote=3.0,
                               description='made in VN')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
