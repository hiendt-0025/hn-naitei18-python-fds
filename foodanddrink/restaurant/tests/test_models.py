from django.test import TestCase
from ..models import Order, OrderDetail, User, Product, Category, Customer

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


class ProductModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    category = Category.objects.create(name = "Drinks")
    Product.objects.create(name="product1", category = category, description= "test product", price= 2, quantity=10, vote= 4)

  def test_name_label(self):
    product = Product.objects.get(id=1)
    field_label = product._meta.get_field('name').verbose_name
    self.assertEquals(field_label, 'name')

  def test_name_max_length(self):
    product = Product.objects.get(id=1)
    max_length=product._meta.get_field('name').max_length
    self.assertEquals(max_length,200)

  def test_object_name_is_name(self):
    product = Product.objects.get(id=1)
    expected_object_name = f'{product.name}'
    self.assertEquals(expected_object_name, str(product))

  def test_get_absolute_url(self):
    product = Product.objects.get(id=1)
    self.assertEquals(product.get_absolute_url(), '/restaurant/product/1')

  def test_price_max_digits(self):
    product = Product.objects.get(id=1)
    max_digits=product._meta.get_field('price').max_digits
    self.assertEquals(max_digits,4)

  def test_price_decimal_places(self):
    product = Product.objects.get(id=1)
    decimal_places=product._meta.get_field('price').decimal_places
    self.assertEquals(decimal_places,2)

  def test_vote_value(self):
    product = Product.objects.get(id=1)
    if float(product.vote)>5:
      raise ValidationError(_('Product rating beyond 5'))
    elif int(product.vote<0):
      raise ValidationError(_('Product rating under 0'))


class CustomerModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username = 'Test', password ='123123@q')
    Customer.objects.create(user=user, address="So 1 , ngo 1", phone_number= "0987654321")

  def test_object_name_is_user_name(self):
    customer = Customer.objects.get(id=1)
    expected_object_name = f'{customer.user.username}'
    self.assertEquals(expected_object_name, str(customer))
