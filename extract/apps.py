from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class ExtractConfig(AppConfig):
    name = 'extract'
    def ready(self):
        #from .views import keyword_saved_handler
        from .views import KeywordView
        from .models import Keyword, StopWord
        post_save.connect(KeywordView.add_keyword, sender=Keyword)
        post_delete.connect(KeywordView.delete_keyword, sender=Keyword)

        post_save.connect(KeywordView.add_stop_word, sender=StopWord)
        post_delete.connect(KeywordView.delete_stop_word, sender=StopWord)

