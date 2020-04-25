from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=264, default='')
    occupation = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
#
# class Document(models.Model):
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to='documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
class Question(models.Model):
    title = models.CharField(max_length=264)
    slug = models.SlugField(max_length=264)
    content = models.TextField(default='')
    author = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home:view_question', args=[self.slug])

    def __str__(self):
        return self.title

class Answer(models.Model):
    question=models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user= models.CharField(max_length=250)
    email=models.EmailField()
    body=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    # upvotes=models.BooleanField(default='0')
    def approved(self):
        self.approved =True
        self.save()

    def __str__(self):
        return self.user
