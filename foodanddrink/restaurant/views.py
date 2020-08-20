from django.shortcuts import render
from django.utils.translation import ugettext as _

def index(request):
  return render(request, 'index.html')
