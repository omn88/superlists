from django.conf.urls import url

from lists import views

app_name = 'lists'
urlpatterns = [

    url(r'^$', views.home_page, name='home_page'),
	url(r'^lists/new$', views.new_list, name='new_list'),
	url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
	url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),
]