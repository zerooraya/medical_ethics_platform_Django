from django.contrib import admin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['title', 'author', 'category', 'status', 'created_at']
    list_filter   = ['status', 'category']
    search_fields = ['title', 'content']
    actions       = ['approve', 'reject']

    def approve(self, request, queryset):
        queryset.update(status='approved')
    approve.short_description = 'Approve selected posts'

    def reject(self, request, queryset):
        queryset.update(status='rejected')
    reject.short_description = 'Reject selected posts'
