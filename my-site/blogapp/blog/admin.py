from django.contrib import admin
from django.db import models
from .models import Blog, Category, Comment
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse






# Register your models here.



class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_home", "slug", "selected_categories")
    list_editable = ("is_active", "is_home")
    search_fields = ("title", "description")
    readonly_fields = ("slug",)
    list_filter = ("is_active", "is_home","categories")


    def selected_categories(self, obj):
        html = "<ul>"

        for category in obj.categories.all():
            html += "<li>" + category.name + "</lis>"
        
        html += "</ul>"
        return mark_safe(html)
    selected_categories.short_description = 'Seçili Kategoriler'






class CommentAdmin(admin.ModelAdmin):
    
    list_display = ('blog', 'author', 'content', 'created_at', 'updated_at')
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

    def get_queryset(self, request):
        
        sorgu_kümesi = super().get_queryset(request)
        
        if request.user.is_superuser:
            return sorgu_kümesi
        return sorgu_kümesi.filter(author=request.user)
    
    
    def save_model(self, request, obj, form, change):
        if  not change or obj.author == request.user:
            super().save_model(request, obj, form, change)



admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
