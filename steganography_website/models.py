from django.db import models

class StegoObjctStore(models.Model):
	name = models.CharField('name', max_length = 50)
	image = models.ImageField(upload_to = "images/")

	def __str__(self):
		return self.name
