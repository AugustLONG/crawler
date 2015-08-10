# coding=utf-8
from django.contrib import admin
from search.models import Category, Link, Tag
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Permission


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'order', 'parent', 'enabled')
    list_editable = ('name', 'slug', 'order', 'enabled')
    search_fields = ('name', 'slug')  # 添加search bar，在指定的字段中search
    filter_horizontal = ('tags',)
    raw_id_fields = ('parent',)
    ordering = ('order',)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'url', 'order', 'enabled')
    list_editable = ('name', 'url', 'order', 'enabled')
    search_fields = ('name', 'url')  # 添加search bar，在指定的字段中search
    ordering = ('order',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'hot', 'enabled')
    list_editable = ('name', 'slug', 'hot', 'enabled')
    search_fields = ('name', 'slug')  # 添加search bar，在指定的字段中search
    ordering = ('name',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'codename', 'content_type',)
    search_fields = ('name', 'codename')  # 添加search bar，在指定的字段中search


class ExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published',)
    readonly_fields = ('show_url',)
    list_filter = ('created',)  # 页面右边会出现相应的过滤器选项
    # filter_horizontal = ('authors',)
    # raw_id_fields = ('publisher',)

    def show_url(self, instance):
        url = reverse('article_detail', kwargs={'pl': instance.pk})
        response = format_html("""<a href="{0}">文章预览preview</a>""", url)
        return response

    show_url.short_description = u"文章预览"
    # 显示HTML tag
    # 对于用户提交的数据, 永远不要这么设置!
    show_url.allow_tags = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Permission, PermissionAdmin)