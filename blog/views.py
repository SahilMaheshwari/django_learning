from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author' : 'Mahil Saheshwari',
        'title'  : 'Make online ps please',
        'content': 'Pleleeeazzeeeee',
        'date'   : '7 may 2010'
    },
    {
        'author' : 'Drums mAN',
        'title'  : 'I love drums man',
        'content': 'Ba dum tss',
        'date'   : '31 Aug 2015'
    }
]


def home(request):
    context = {
        'posts' : posts
        }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})