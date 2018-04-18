from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     #output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# class IndexView(generic.ListView):
#     template_name = 'index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]

# from .forms import NameForm
# from django.views.generic.edit import FormMixin



# class DetailView(generic.DetailView):
#     #form_class = NameForm
#     #model = Question
#     template_name = 'detail.html'


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'results.html'

# def example (request):
#     return render_to_response('example.html')

# def login_auth(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     print(user)
@login_required
def index(request):
    return render(request, 'detail.html')

# def custom_login(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('/')
#     else:
#         return login(request)
    
import sys
import os
import jieba
import jieba.analyse

jieba.load_userdict("./extract/dict_with_cnt.txt")
jieba.analyse.set_stop_words("./extract/ntub_stop_words.txt")

from django.http import JsonResponse
@login_required
def vote(request):
    try:
        article = request.POST.get('article')
        title = request.POST.get('title')
        if title:
            article = (title + '\n')*10 + article

        tags = jieba.analyse.extract_tags(article, topK=15, withWeight=True)

        return JsonResponse({'tags':tags})
    except (KeyError):
        return JsonResponse({'tags':''})
