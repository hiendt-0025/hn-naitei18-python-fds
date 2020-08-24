from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Customer, Product, Order, Category, OrderDetail
UserModel = get_user_model()
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from restaurant.models import Customer, Category, Product
from django.http import Http404
from django.core.paginator import Paginator

# view.function
def index(request):
  list_category = Category.objects.all()
  list_product = Product.objects.filter(vote = 5)
  paginator = Paginator(list_product, 4)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'list_category': list_category,
    'page_obj': page_obj
  }

  return render(request, 'index.html', context)

def success_activation(request):
  return render(request, 'sign_up/verification_success.html')

def fail_activation(request):
  return render(request, 'sign_up/verification_fail.html')

def inform(request):
  return render(request, 'sign_up/inform_to_verify.html')

def register(request):
  if request.method == 'GET':
    return render(request, 'sign_up/register.html')
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()
      current_site = get_current_site(request)
      mail_subject = 'Activate your account.'
      message = render_to_string('sign_up/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
      })
      to_email = form.cleaned_data.get('email')
      email = EmailMessage(
        mail_subject, message, to=[to_email],
      )
      email.content_subtype = "html"
      email.send()
      return HttpResponseRedirect(reverse('inform'))
  else:
    form = SignUpForm()
  return render(request, 'sign_up/register.html', {'form': form})


def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = UserModel._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('success_activation'))
  else:
    return HttpResponseRedirect(reverse('fail_activation'))

@login_required
def profile(request):
  try:
    customer = Customer.objects.filter(user = request.user)
  except Customer.DoesNotExist:
    raise Http404('Customer does not exist')

  context = {
    'profile': customer
  }
  return render(request, 'restaurant/profile.html', context)
# def order(request):
#   return render(request,'restaurant/checkout.html')

def order_detail_view(request, pk):
  customer_order = Order.objects.get(pk=pk)
  items_in_cart = OrderDetail.objects.filter(order=pk).select_related("product")
  return render(request,'restaurant/checkout.html', context={'customer_order': customer_order, 'items_in_cart': items_in_cart})

def delete_a_product(request, pk, pk2):
    deleted_product = OrderDetail.objects.filter(order=pk).filter(pk=pk2)
    deleted_product.delete()
    return HttpResponseRedirect(reverse('success_activation'))
