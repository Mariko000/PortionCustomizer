# profanity_filter/admin.py

from django.contrib import admin
from .models import NgWord

@admin.register(NgWord)
class NgWordAdmin(admin.ModelAdmin):
    list_display = ('word',)