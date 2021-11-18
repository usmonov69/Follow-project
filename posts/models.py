from django.db import models
from django.core.validators import FileExtensionValidator

from profiles.models import Profile

class Post(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	image = models.ImageField(upload_to='posts/', validators=[FileExtensionValidator(['png','jpg','jpeg'])], blank=True )
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.title[:20])

	class Meta:
		ordering = ['-created']


	def get_absolute_url(self):
		return reverse('detail-post', kwargs={
			'id': self.id
			})





	# validators=[FileExtensionValidator(['png','jpg','jpeg'])], blank=True )