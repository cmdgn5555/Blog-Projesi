from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)

    
    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blogs")
    video_file = models.FileField(upload_to="videos")         
    description = RichTextField()
    is_active = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    until_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(max_length=1000, default="")
    categories = models.ManyToManyField(Category, blank=True)
    #category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.title}"
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)




class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='yorumlar', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="yorum_begen", blank=True)
    dislikes = models.ManyToManyField(User, related_name="yorum_begenme", blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='yanitlar', on_delete=models.CASCADE)
   

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def __str__(self):
        return self.content













 
  


        




