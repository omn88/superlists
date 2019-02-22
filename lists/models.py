from django.db import models

# Create your models here.

class List(models.Model):
	text = models.TextField(default='')
	list_name = models.TextField(default='')
	
	def __str__(self):
		return self.list_name
	
class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default = None)
	
	def __str__(self):
		return self.text