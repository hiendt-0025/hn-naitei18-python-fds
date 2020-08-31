from django.test import TestCase

from ..models import Order, OrderDetail, User, Product, Category


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin1 = User.objects.create(is_superuser=1, username="admin1", first_name="hoang", last_name="thanh",
                                    email="admin1@admin1.com", is_staff=1, is_active=1)
        Order.objects.create(total_price=100, status="p", admin_id=admin1.id, customer_id=1,
                             code="2020_9_14_xx")

    def test_checkTotalPrice(self):
        print("Checking total_price field of Order.")
        test_order = Order.objects.get(id=1)
        max_digits = test_order._meta.get_field('total_price').max_digits
        self.assertEquals(max_digits, 6)


class OrderDetailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin2 = User.objects.create(is_superuser=1, username="admin2", first_name="hoang", last_name="thanh",
                                     email="admin2@admin2.com", is_staff=1, is_active=1)
        Order.objects.create(total_price=100, status="p", admin_id=admin2.id, customer_id=1,
                             code="2020_9_14_xx")
        Category.objects.create(name='Drinks')
        Product.objects.create(name='milk tea', category_id=1, price=23.00, quantity=10, vote=3.0,
                               description='made in VN')
        OrderDetail.objects.create(price=10, amount=10, order_id=1, product_id=1)

    def test_checkPrice(self):
        print("Checking price field of OrderDetail.")
        test_orderdetail = OrderDetail.objects.get(id=1)
        max_digits = test_orderdetail._meta.get_field('price').max_digits
        print(max_digits)
        self.assertEquals(max_digits, 4)
