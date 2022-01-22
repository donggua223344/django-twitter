from django.contrib import admin
from likes.models import Like


# admin.py是用来规定后台管理员可以看到什么，以及可以做什么的文件
# /admin是直接访问数据库的一个UI接口，和Django提供的，和API代码没有关系
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
