from django.contrib import admin
from .models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ("name",)}

admin.site.register(Category, CategoryAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display= ('title', 'url', 'views', 'category')
    search_fields = ('title',)
    autocomplete_fields = ('category',)

admin.site.register(Page, PageAdmin)

admin.site.register(UserProfile)