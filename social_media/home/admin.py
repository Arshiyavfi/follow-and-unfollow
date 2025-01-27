from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body',)
    list_filter = ('updated', 'created', 'slug')
    prepopulated_fields = {'slug':('body',)}
