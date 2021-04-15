from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse



from django.utils.timezone import now




class Category(models.Model):
    name = models.CharField(max_length=50, blank=True)
    slug = models.CharField(max_length=50, blank=True)
    picture = models.FileField(blank=True, null=True)


    def __str__(self):
        return self.name




# Create your models here.
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    profile_pic = models.FileField()
    about = models.TextField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=55, default="restor")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    timeStamp = models.DateTimeField(default=now)
    about= RichTextField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    cover_pic = models.FileField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts')


class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)




class contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    subject = models.TextField()
    text = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
