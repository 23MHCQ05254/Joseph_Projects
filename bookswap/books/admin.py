from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'semester', 'price', 'condition', 'available')
    list_filter = ('department', 'semester', 'condition', 'available')
    search_fields = ('title', 'author', 'subject')
