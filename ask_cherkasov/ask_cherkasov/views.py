from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse

def base(request):
  return render(request, 'base.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : '12345', })

def index(request):
  return render(request, 'index.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : '12345', 'questions' : '0123456789', 'tags_count' : '123', })

def question(request):
  return render(request, 'question.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : '12345', 'answers' : '1234567', 'correct' : '5', 'tags_count' : '123', 'author_auth' : False, })

def ask(request):
  return render(request, 'ask.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : '12345', 'errs' : False, })

def login(request):
  return render(request, 'login.html', { 'test_auth' : False, 'best_users' : '1234567', 'hot_tags' : '12345', 'errs' : False, })

def signup(request):
  return render(request, 'signup.html', { 'test_auth' : False, 'best_users' : '1234567', 'hot_tags' : '12345', 'errs' : False, })

def edit(request):
  return render(request, 'profile_edit.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : '12345', 'errs' : False, })

def hello_world(request):
  endl = '<br\>'
  rstring = 'Hello world!' + endl
  for key, val in request.GET.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  for key, val in request.POST.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  return HttpResponse(rstring)
