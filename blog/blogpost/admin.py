from django.contrib import admin
from .models import CustomUser, Post, BlogComment, Category, contact

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(BlogComment)
admin.site.register(Category)
admin.site.register(contact)