from decimal import Decimal
import datetime

from cart.cart import Cart
from cart.context_processor import cart_total_amount

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from .models import Customer, Category, Product, OrderDetail, Order
from django.http import Http404
from django.core.paginator import Paginator
from django.views import generic

UserModel = get_user_model()
DEFAULT_AVATAR = 'media/profile_pics/default.jpg'
# view.function
def index(request):
    list_category = Category.objects.all()
    list_product = Product.objects.filter(vote=5)
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
        customer = Customer(user_id = user.id, avatar = DEFAULT_AVATAR)
        customer.save()
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


class ProductDetailView(generic.DetailView):
    model = Product
    def product_detail_view(request, primary_key):
        product = get_object_or_404(Product, pk=primary_key)
        return render(request, 'restaurant/product_detail.html', context={'product': product})


@login_required
def cart_add(request, pk):
    cart = Cart(request)
    product = Product.objects.get(id=pk)
    cart.add(product=product, category=product.category.name)
    return HttpResponseRedirect(reverse('index'))


@login_required
def cart_detail(request):
    return render(request, 'restaurant/checkout.html', context= cart_total_amount(request))


@login_required
def item_clear(request,pk):
    cart = Cart(request)
    product = Product.objects.get(id=pk)
    cart.remove(product)
    return HttpResponseRedirect(reverse('order'))


@login_required
def make_order(request):
    if bool(request.session['cart']):
        today = datetime.datetime.now()
        try:
            latest_order = Order.objects.latest('id')
        except Order.DoesNotExist:
            latest_order = None
        if latest_order is None:
            order_code = 1
        else:
            order_code = latest_order.id + 1

        code = str(today.year) +"_"+ str(today.month) +"_"+ str(today.day) +"_"+ str(order_code)
        cart = Cart(request)
        customer = Customer.objects.get(user_id=request.user.id)
        total_bill = 0.0
        for key, value in request.session['cart'].items():
            total_bill = total_bill + (float(value['price']) * value['quantity'])

        order = Order(total_price=Decimal(total_bill), code=code, status='p', admin_id=1,
                      customer_id=customer.id)
        order.save()

        order_id = order.id

        for key, item in request.session['cart'].items():
            ordered_item = OrderDetail(price=Decimal(item['price']), amount=item['quantity'],
                                       product_id=item['product_id'], order_id=order_id)
            ordered_item.save()

        cart.clear()
    return HttpResponseRedirect(reverse('index'))


def item_decrement(request, pk):
    cart = Cart(request)
    product = Product.objects.get(id=pk)
    cart.decrement(product=product)
    return HttpResponseRedirect(reverse('order'))


def item_increment(request, pk):
    cart = Cart(request)
    product = Product.objects.get(id=pk)
    cart.add(product=product, category=product.category.name)
    return HttpResponseRedirect(reverse('order'))
