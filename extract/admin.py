from django.contrib import admin
from .models import Keyword, StopWord
# Register your models here.

@admin.register(Keyword)
class KeywordsAdmin(admin.ModelAdmin):
    search_fields = ['keyword']

@admin.register(StopWord)
class StopWordsAdmin(admin.ModelAdmin):
    search_fields = ['stop_word']