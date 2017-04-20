from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from random import randint
from ask_cherkasov import miscellaneous

class Tag:
  def __init__(self, oid, tag, color):
    self._id = oid
    self._tag = tag
    self._color = color
  def __repr__(self):
    return repr(self._id, self._tag, self._color)
  def __str__(self):
    return str(self._tag)
  def get_url(self):
    return reverse('tag', kwargs={ 'tag' : self._tag, })
  def id(self):
    return self._id
  def tag(self):
    return self._tag
  def color(self):
    return self._color

class Question:
  def __init__(self, oid, title, text, tags, rating):
    self._id = oid
    self._title = title
    self._text = text
    self._tags = tags
    self._rating = rating
  def __repr__(self):
   return repr(self._id, self._title, self._text, self._tags, self._rating)
  def id(self):
    return self._id
  def title(self):
    return str(self._title);
  def text(self):
    return str(self._text);
  def tags(self):
    return self._tags;
  def rating(self):
    return self._rating;
  def get_url(self):
    return reverse('question', kwargs={ 'id': self._id, })

class Answer:
  def __init__(self, oid, text, rating):
    self._id = oid
    self._text = text
    self._rating = rating
  def __repr__(self):
    return repr(self._id, self._text, self._rating)
  def id(self):
    return self._id
  def text(self):
    return self._text
  def rating(self):
    return self._rating

def base(request):
  return render(request, 'base.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : '12345', })

def newest(request):
  questions = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 100):
    tags = []
    for j in range(1, 5):
      tag_id = j + randint(0, 5)
      tags.append(
        Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)])
      )
    questions.append(Question(i, 'Заголовок вопроса ' + str(i), 'Текст вопроса ' + str(i), tags, randint(-20, 20)))
  questions.sort(key = lambda question: question._id, reverse = True)
  pagination = miscellaneous.paginate(questions, request, key='question')
  tags = []
  for i in range(1, 5):
    tag_id = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  return render(request, 'index.html', { 'title' : 'Новые вопросы', 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : tags, 'questions' : pagination, })

def hottest(request):
  questions = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 100):
    tags = []
    for j in range(1, 5):
      tag_id = j + randint(0, 5)
      tags.append(
        Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)])
      )
    questions.append(Question(i, 'Заголовок вопроса ' + str(i), 'Текст вопроса ' + str(i), tags, randint(-20, 20)))
  questions.sort(key = lambda question: question._rating, reverse = True)
  pagination = miscellaneous.paginate(questions, request, key='question')
  for i in range(1, 5):
    tag_id = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  return render(request, 'index.html', { 'title' : 'Популярные вопросы', 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : tags, 'questions' : pagination, })

def by_tag(request, tag):
  tags = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 10):
    tags.append(Tag(i, 'Тег' + str(i), colors[i % len(colors)]))
  questions = []
  for i in range(1, 100):
    q_tags = [Tag(1, str(tag), colors[0]),]
    for j in range(2, 6):
      tag_id = j + randint(0, 4)
      q_tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
    questions.append(Question(i, 'Заголовок вопроса ' + str(i), 'Текст вопроса ' + str(i), q_tags, randint(-20, 20)))
    questions.sort(key = lambda question: question._rating, reverse = True)
    pagination = miscellaneous.paginate(questions, request, key='question')
  return render(request, 'index.html', { 'title' : 'Тег ' + str(tag), 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : tags, 'questions' : pagination, })

def question(request, id):
  tags = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 5):
    tag_id  = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  question = Question(int(id), 'Заголовок вопроса ' + str(id), 'Текст вопроса' + str(id), tags, randint(-20, 20))
  answers = []
  for i in range(1, 7):
    answers.append(Answer(i, 'Ответ ' + str(i) + ' на вопрос ' + question._title, randint(-20, 20)))
  return render(request, 'question.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : tags, 'question' : question, 'answers' : answers, 'correct' : '5', 'author_auth' : False, })

def ask(request):
  tags = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 5):
    tag_id  = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  return render(request, 'ask.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : tags, 'errs' : False, })

def login(request):
  tags = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 5):
    tag_id  = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  return render(request, 'login.html', { 'test_auth' : False, 'best_users' : '1234567', 'hot_tags' : tags, 'errs' : False, })

def signup(request):
  tags = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 5):
    tag_id  = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  question = Question(int(id), 'Заголовок вопроса ' + str(id), 'Текст вопроса' + str(id), tags, randint(-20, 20))
  return render(request, 'signup.html', { 'test_auth' : False, 'best_users' : '1234567', 'hot_tags' : '12345', 'errs' : False, })

def edit(request):
  tags = []
  colors = ('default', 'primary', 'success', 'info', 'danger', 'warning')
  for i in range(1, 5):
    tag_id  = i + randint(0, 5)
    tags.append(Tag(tag_id, 'Тег' + str(tag_id), colors[tag_id % len(colors)]))
  return render(request, 'profile_edit.html', { 'test_auth' : True, 'best_users' : '1234567', 'hot_tags' : tags, 'errs' : False, })

def hello_world(request):
  endl = '<br\>'
  rstring = 'Hello world!' + endl
  for key, val in request.GET.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  for key, val in request.POST.items():
    rstring = rstring + str(key) + ' : ' + str(val) + endl
  return HttpResponse(rstring)
