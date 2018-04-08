from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import requests
import jieba.analyse

def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    tags = jieba.analyse.extract_tags(
        '今天的天氣非常好，適合到台灣大學走走，晚上吃拉麵',
        topK=topK, withWeight=False)

    print(tags)
    return HttpResponse('<pre>' + tags + '</pre>')

# Create your views here.
# def index(request):
#     # return HttpResponse('Hello from Python!')
#     return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

