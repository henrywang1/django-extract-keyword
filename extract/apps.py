from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
import jieba
import jieba.analyse

from django.db import connection
def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()

class ExtractConfig(AppConfig):
    name = 'extract'
    def ready(self):
        if not db_table_exists('extract'):
            return 

        from .views import KeywordView
        from .models import Keyword, StopWord
        post_save.connect(KeywordView.add_keyword, sender=Keyword)
        post_delete.connect(KeywordView.delete_keyword, sender=Keyword)

        post_save.connect(KeywordView.add_stop_word, sender=StopWord)
        post_delete.connect(KeywordView.delete_stop_word, sender=StopWord)

        all_keywords = Keyword.objects.all()
        all_stop_words = StopWord.objects.all()

        print('Add keywords, total={0}'.format(len(all_keywords)))
        for k in all_keywords:
            jieba.add_word(str(k), 999, 'n')

        print('Add stopwords, total={0}'.format(len(all_stop_words)))
        for k in all_stop_words:
            jieba.analyse.add_stop_word(str(k))

