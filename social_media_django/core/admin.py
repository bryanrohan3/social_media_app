from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'caption', 'date_time_created']

# Likes
admin.site.register(Like)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'isLiked', 'post']


# Comments
admin.site.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'text', 'date_time_created']

admin.site.register(FriendRequest)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'status', 'date_time_created']

admin.site.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'date_time_created']