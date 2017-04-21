from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from random import randint
from ask_cherkasov import miscellaneous
from ask_cherkasov.models import UserData, Tag, Question, QuestionLike, Answer, AnswerLike

def base(request):
  return render(request, 'base.html', { 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), })

def newest(request):
  questions = Question.objects.newest()
  pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Новые вопросы', 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'questions' : pagination, })

def hottest(request):
  questions = Question.objects.hottest()
  pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Популярные вопросы', 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'questions' : pagination, })

def by_tag(request, tag):
  try:
    obj_tag = Tag.objects.by_tag(tag)
  except Tag.DoesNotExist:
    raise Http404()
  questions = Question.objects.by_tag(obj_tag)
  pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Тег ' + str(tag), 'test_auth' : True, 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'questions' : pagination, })

def question(request, id):
  try:
    question = Question.objects.single(id)
  except Question.DoesNotExist:
    raise Http404()
  return render(request, 'question.html', { 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'question' : question, })

def ask(request):
  return render(request, 'ask.html', { 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'errs' : False, })

def login(request):
  return render(request, 'login.html', { 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'errs' : False, })

def signup(request):
  return render(request, 'signup.html', { 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'errs' : False, })

def edit(request):
  return render(request, 'profile_edit.html', { 'best_users' : UserData.objects.all()[1:10], 'hot_tags' : Tag.objects.get_top_X(), 'errs' : False, })

def hello_world(request):
  endl = '<br\>'
  rstring = 'Hello world!' + endl
  for key, val in request.GET.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  for key, val in request.POST.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  return HttpResponse(rstring)

