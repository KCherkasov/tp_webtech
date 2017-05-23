from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.contrib import auth
from random import randint
from ask_cherkasov import miscellaneous, mod_ajax, decorators
from ask_cherkasov.models import UserData, Tag, Question, QuestionLike, Answer, AnswerLike
from ask_cherkasov.forms import Sign_in, Sign_up, AnswerForm, QuestionForm, ProfileEdit
from ask_cherkasov.decorators import login_required, ajax_login_required

def base(request):
  return render(request, 'base.html')

def newest(request):
  questions = Question.objects.newest()
  pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Новые вопросы', 'questions' : pagination, })

def hottest(request):
  questions = Question.objects.hottest()
  pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Популярные вопросы', 'questions' : pagination, })

def by_tag(request, tag):
  try:
    obj_tag = Tag.objects.by_tag(tag)
  except Tag.DoesNotExist:
    raise Http404()
  questions = Question.objects.by_tag(obj_tag)
  pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Тег ' + str(tag), 'questions' : pagination, })

def question(request, id):
  try:
    question = Question.objects.single(id)
  except Question.DoesNotExist:
    raise Http404()
  if request.method == 'POST':
    answer_form = AnswerForm(request.POST)
    if answer_form.is_valid():
      answer = answer_form.save(question, request.user)
      return HttpResponseRedirect('#answer_' + str(answer.id))
  else:
    answer_form = AnswerForm()
  return render(request, 'question.html', { 'question' : question, 'answer_form' : answer_form, })

@login_required
def ask(request):
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid():
      question = form.save(request.user)
      return HttpResponseRedirect(reverse('question', kwargs = { 'id' : question.id }))
  else:
    form = QuestionForm()
  return render(request, 'ask.html', { 'form' : form, })

@login_required
def logout(request):
  redirect = request.GET.get('continue', '/')
  auth.logout(request)
  return HttpResponseRedirect(redirect)

def login(request):
  redirect = request.GET.get('continue', '/')
  if request.user.is_authenticated():
    return HttpResponseRedirect(redirect)
  if request.method == 'POST':
    form = Sign_in(request.POST)
    if form.is_valid():
      auth.login(request, form.cleaned_data['user'])
      return HttpResponseRedirect(redirect)
    else:
      return HttpResponseRedirect(reverse('login'))
  else:
    form = Sign_in()
  return render(request, 'login.html', { 'form' : form, })

def signup(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  if request.method == 'POST' :
    form = Sign_up(request.POST, request.FILES)
    if form.is_valid():
      user = form.save()
      auth.login(request, user)
      return HttpResponseRedirect('/')
  else:
    form = Sign_up()
  return render(request, 'signup.html', { 'form' : form, })

@login_required
def edit(request):
  if request.method == 'POST':
    form = ProfileEdit(request.POST)
    if form.is_valid():
      form.save(request.user)
      return HttpResponseRedirect('')
  else:
    user = model_to_dict(request.user)
    user_data = request.user.userdata
    user['about'] = user_data.about
    form = ProfileEdit(user)
  return render(request, 'profile_edit.html', { 'form' : form, 'user' : request.user })

@ajax_login_required
@require_POST
def ajax_question_like(request, id):
  try:
    question = Question.objects.get(pk = id)
    value = int(request.POST.get('value', QuestionLike.LIKE))
    if value != QuestionLike.LIKE and value != QuestionLike.DISLIKE:
      value = QuestionLike.LIKE
    QuestionLike.objects.add(author = request.user, question = question, value = value)
    question = Question.objects.get(pk = id)
    return mod_ajax.HttpResponseAjax(likes = question.likes, question_id = question.id)
  except Question.DoesNotExist:
    return mod_ajax.HttpResponseAjaxError(code = 'no_question', message = 'Такого вопроса не существует')
  except QuestionLike.AlreadyLike as ex_1:
    return mod_ajax.HttpResponseAjaxError(code = 'already_like', message = str(ex_1))
  except QuestionLike.OwnLike as ex_2:
    return mod_ajax.HttpResponseAjaxError(code = 'own_like', message = str(ex_2))

@ajax_login_required
@require_POST
def ajax_answer_like(request, id):
  try:
    answer = Answer.objects.get(pk = id)
    value = int(request.POST.get('value', AnswerLike.LIKE))
    if value != AnswerLike.LIKE and value != AnswerLike.DISLIKE:
      value = AnswerLike.LIKE
    AnswerLike.objects.add(author = request.user, answer = answer, value = value)
    answer = Answer.objects.get(pk = id)
    return mod_ajax.HttpResponseAjax(likes = answer.likes, answer_id = answer.id)
  except AnswerLike.DoesNotExist:
    return mod_ajax.HttpResponseAjaxError(code = 'no_answer', message = 'Такого ответа не существует')
  except AnswerLike.AlreadyLike as ex_1:
    return mod_ajax.HttpResponseAjaxError(code = 'already_like', message = str(ex_1))
  except AnswerLike.OwnLike as ex_2:
    return mod_ajax.HttpResponseAjaxError(code = 'own_like', message = str(ex_2))

@ajax_login_required
@require_POST
def ajax_answer_correct(request, id):
  try:
    answer = Answer.objects.get(pk = id)
    answer.set_correct(request.user)
    return mod_ajax.HttpResponseAjax(answer_id = answer.id)
  except Answer.DoesNotExist:
    return mod_ajax.HttpResponseAjaxError(code = 'no_answer', message = 'Такого ответа не существует')
  except Exception as ex:
    return mod_ajax.HttpResponseAjaxError(code='error', message = ex.message)

def hello_world(request):
  endl = '<br\>'
  rstring = 'Hello world!' + endl
  for key, val in request.GET.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  for key, val in request.POST.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  return HttpResponse(rstring)
