from django.contrib import admin
from .models import Article

# Register your models here.

class Date(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Article,Date)