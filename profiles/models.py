from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


GENDER_CHOICES = (
	('Male', 'Male'),
	('Female', 'Female'),
	)

# def save_avatar(self):
# 		gender = self.gender
# 		if gender == 'Male':
# 			avatar = 'male.png'
# 		else:
# 			avatar = 'female.png'
# 		return avatar
 
class Profile(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50, blank=True)
	bio = models.CharField(max_length=100, default="no bio...")
	email = models.EmailField(max_length=100, blank=True)
	avatar = models.ImageField( default='avatar.png', upload_to='avatars/' )
	friends = models.ManyToManyField(User, related_name='friends', blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=6 , choices=GENDER_CHOICES)
	slug = models.SlugField(unique=True, blank=True)
	birth_date = models.DateField(auto_now_add=False, null=True)
	join_date = models.DateTimeField(auto_now_add=True)

	def profiles_posts(self):
		return self.post_set.all()

	def __str__(self):
		return str(self.user.username)

	def get_friends(self):
		return self.friends.all()

	def get_friends_num(self):
		return self.friends.all().count()

	# def profiles_posts(self):
	# 	return self.post_set.all()

	def get_profile_post_num(self):
		return self.post_set.all().count()

	# def get_absolute_url(self):
	# 	return reverse('profiles:profile-detail', kwargs={
	# 		'slug':self.slug
	# 		})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user.username)
		return super().save(*args, **kwargs)


	# def save_avatar(instance):
	# 	gender = instance.gender
	# 	if gender == 'Male':
	# 		avatar = 'male.png'
	# 	else:
	# 		avatar = 'female.png'
	# 	return avatar
# python manage.py makemigrations
STATUS_CHOICES = (
	('send', 'send'),
	('accepted', 'accepted'),
	)

class Relationship(models.Model):
	sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
	status = models.CharField(max_length=8, choices=STATUS_CHOICES)
	update_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f"{self.sender}-{self.receiver}-{self.status}"




