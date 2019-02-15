from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


def home_page(request):
	return HttpResponse('<html><title>To-Do lists</title></html>')
