from django.contrib import admin
from likes.models import Like


# admin.py是用来规定后台管理员可以看到什么，以及可以做什么的文件
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'content_type',
        'object_id',
        'content_object',
        'created_at',
    )
    list_filter = ('content_type',)
    date_hierarchy = 'created_at'
