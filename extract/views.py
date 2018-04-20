from django.shortcuts import  render
from .models import Keyword
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    return render(request, 'detail.html')
    
import sys
import os
import jieba
import jieba.analyse
from django.db.models import Max

# Now, we load user dict and stop words from db
# jieba.load_userdict("./extract/dict_with_cnt.txt")
# jieba.analyse.set_stop_words("./extract/ntub_stop_words.txt")

from django.http import JsonResponse
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


def keyword_saved_handler(sender, instance, **kwargs):
    print("post_save finished!")


class KeywordView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        for k in Keyword.objects.all():
            jieba.add_word(str(k), 999, 'n')
        self.login_url = '/login/'

    def post(self, request):
        try:
            article = request.POST.get('article')
            title = request.POST.get('title')
            if title:
                article = (title + '\n')*10 + article
            tags = jieba.analyse.extract_tags(article, topK=15, withWeight=True)
            return JsonResponse({'tags':tags})
        except (KeyError):
            return JsonResponse({'tags':''})

    @staticmethod
    def add_keyword(sender, instance, **kwargs):
        #print('add ' + str(instance))
        jieba.add_word(str(instance), 999, 'n')
    
    @staticmethod
    def delete_keyword(sender, instance, **kwargs):
        #print('delete ' + str(instance))
        jieba.del_word(str(instance))
    
    @staticmethod
    def add_stop_word(sender, instance, **kwargs):
        #print('add stop ' + str(instance))
        jieba.analyse.add_stop_word(str(instance))
    
    @staticmethod
    def delete_stop_word(sender, instance, **kwargs):
        #print('delete stop' + str(instance))
        jieba.analyse.add_stop_word(str(instance))