from django.shortcuts import  render
from .models import Keyword, StopWord
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .trend import word_related

# 摘要生成
# from .pointer_generator.write_bin import write_to_bin 
# from .pointer_generator.inference import inference
# from tensorflow.python import debug as tf_debug
# 摘要生成
# def abstract(request):
#     return render(request, 'abstract.html')

@login_required
def index(request):
    return render(request, 'detail.html')

import sys
import os
from django.db.models import Max

import jieba
import jieba.analyse
# Now, we load user dict and stop words from db
# jieba.load_userdict("./extract/dict_with_cnt.txt")
# jieba.analyse.set_stop_words("./extract/ntub_stop_words.txt")
from django.http import JsonResponse


class TrendView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            tags = request.POST.get('tags')
            tags = tags.split(',')
            for t in tags:
                print(t)
            print(tags)
            if tags:
                ret = (word_related(tags))
                return JsonResponse({'trend': ret})
        except (KeyError):
            return JsonResponse({'trend':''})

class KeywordView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        self.login_url = '/login/'

    def post(self, request):
        try:
            article = request.POST.get('article')
            title = request.POST.get('title')
            if title:
                article = (title + '\n')*10 + article
            tags = jieba.analyse.extract_tags(article, topK=15, withWeight=True)
            return JsonResponse({'tags': tags})
        except (KeyError):
            return JsonResponse({'tags':''})

    @staticmethod
    def add_keyword(sender, instance, **kwargs):
        jieba.add_word(str(instance), 999, 'n')
    
    @staticmethod
    def delete_keyword(sender, instance, **kwargs):
        jieba.del_word(str(instance))
    
    @staticmethod
    def add_stop_word(sender, instance, **kwargs):
        jieba.analyse.add_stop_word(str(instance))
    
    @staticmethod
    def delete_stop_word(sender, instance, **kwargs):
        jieba.analyse.del_stop_word(str(instance))

# class AbstractView(LoginRequiredMixin, View):
#     def __init__(self, *args, **kwargs):
#         self.login_url = '/login/'

#     def post(self, request):
#         try:
#             article = request.POST.get('article')
#             print('article: ',article)
#             write_to_bin(article)
#             abstract = inference()
#             return JsonResponse({'abstract': abstract})
#         except (KeyError):
#             return JsonResponse({'abstract':''})
