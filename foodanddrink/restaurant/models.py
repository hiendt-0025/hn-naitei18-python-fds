from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
  """Model representing a category"""
  name = models.CharField(max_length=200, help_text='Enter category name')

  def __str__(self):
    return self.name


class Product(models.Model):
  """docstring for Product"""
  name = models.CharField(max_length=200)
  category = models.ForeignKey('Category', on_delete=models.CASCADE)
  image = models.ImageField(default=None, upload_to='media/product_pics', null=True)
  description = models.TextField(max_length=1000, help_text='Enter description of product')
  price = models.DecimalField(max_digits = 4, decimal_places =2)
  quantity = models.IntegerField()
  vote = models.FloatField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('product-detail', args=[str(self.id)])


class OrderDetail(models.Model):
  """docstring for OrderDetail"""
  product = models.ForeignKey('Product', on_delete=models.CASCADE)
  price = models.DecimalField(max_digits = 4, decimal_places =2)
  order = models.ForeignKey('Order', on_delete= models.CASCADE)
  amount = models.IntegerField()

  def __str__(self):
    return self.product.name


class Order(models.Model):
  """docstring for Order"""
  customer = models.ForeignKey('Customer', on_delete= models.CASCADE)
  admin = models.ForeignKey(User, on_delete= models.CASCADE)
  date_ordered = models.DateTimeField(default=timezone.now)
  total_price = models.DecimalField(max_digits = 6, decimal_places=2, null=True)
  code = models.CharField(max_length=200)

  ORDER_STATUS = (
    ('p', 'PENDING'),
    ('f', 'FINISH'),
    ('c', 'CANCEL'),
  )

  status = models.CharField(
    max_length=1,
    choices=ORDER_STATUS,
    blank=True,
    default='p',
  )

  def __str__(self):
    return f'Order #{self.code}'

  class Meta():
    ordering = ['-date_ordered']


class Review(models.Model):
  """docstring for Review"""
  user = models.ForeignKey('Customer', on_delete= models.CASCADE)
  product = models.ForeignKey('Product', on_delete= models.CASCADE)
  content = models.TextField(max_length=1000, help_text='Enter description of review')
  vote = models.IntegerField()

class Comment(models.Model):
  """docstring for Comment"""
  user = models.ForeignKey('Customer', on_delete= models.CASCADE)
  review = models.ForeignKey('Review',on_delete= models.CASCADE)
  content = models.TextField(max_length=1000, help_text='Enter content of comment')


class Customer(models.Model):
  """docstring for Customer"""
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  avatar = models.ImageField(default=None, upload_to='media/profile_pics', null=True)
  address = models.CharField(max_length=200, blank=True ,null=True)
  phone_number = models.CharField(max_length=200, blank=True ,null=True)

  def __str__(self):
    return f'{self.user.username}'
