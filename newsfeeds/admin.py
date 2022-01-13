from django.contrib import admin
from newsfeeds.models import NewsFeeds


# Register your models here.
@admin.register(NewsFeeds)
class NewsFeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    date_hierarchy = 'created_at'
