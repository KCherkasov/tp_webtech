# -*- coding: utf-8/ -*-

from django.db import models
from django.contrib.auth.models import User

import datetime
from django.utils import timezone
from django.db.models import Count, Sum

from django.core.urlresolvers import reverse

from random import choice
from ask_cherkasov import settings

import os

#-- Extended user model --#

class UserData(models.Model):
  user = models.OneToOneField(User)
  avatar = models.ImageField(upload_to = 'avatars')
  about = models.TextField()

  def avatar_url(self):
    if self.avatar and hasattr(self.avatar, 'url'):
      return self.avatar.url
    else:
      return os.path.join(settings.MEDIA_URL, 'avatars', 'user-noavatar.gif')

  def __str__(self):
    return "[" + str(self.user.id) + "] " + self.user.username

#-- Extended user model end --#

#-- Tags --#

#---- Tags manager ----#

class TagManager(models.Manager):
  def questions_count(self):
    return self.annotate(questions_count = Count('question'))

  def order_by_questions_count(self):
    return self.questions_count().order_by('-questions_count')

  def by_tag(self, tag):
    return self.get(tag = tag)

  def get_or_create(self, tag):
    try:
      tag_obj = self.by_tag(tag)
    except Tag.DoesNotExist:
      tag_obj = self.create(tag = tag, colors = choice(Tag.COLORS)[0])
    return tag_obj

  def get_top_X(self, top_size=10):
    real_top = top_size
    return self.order_by_questions_count()[:real_top]

#---- Tags manager end ----#

#---- Tags model ----#

class Tag(models.Model):
  GREEN = 'success'
  DBLUE = 'primary'
  BLACK = 'default'
  RED = 'danger'
  LBLUE = 'info'
  COLORS = (('GR', GREEN), ('DB', DBLUE), ('B', BLACK), ('RE', RED), ('BL', LBLUE))
    
  tag = models.CharField(max_length=30)
  color = models.CharField(max_length=2, choices=COLORS, default=BLACK)

  objects = TagManager()

  def get_url(self):
    return reverse('tag', kwargs={'tag': self.tag})

  def __str__(self):
    return "[" + str(self.id) + "] " + self.tag

#---- Tags model end ----#

#-- Tags end --#

#-- Questions --#

#---- Querysets ----#

class QuestionQueryset(models.QuerySet):
  def with_tags(self):
    return self.prefetch_related('tags')

  def with_answers(self):
    query = self.prefetch_related('answer_set')
    query = self.prefetch_related('answer_set__author')
    query = self.prefetch_related('answer_set__author__userdata')
    return query

  def with_answers_count(self):
    return self.annotate(ans_count=Count('answer__id', distinct = True))

  def with_author(self):
    return self.select_related('author').select_related('author__userdata')

  def hottest(self):
    return self.order_by('-likes')

  def with_date_later(self, date):
    return self.filter(pub_date__gt=date)

#---- Querysets end ----#

#---- Questions manager ----#

class QuestionManager(models.Manager):
  def queryset(self):
    query = QuestionQueryset(self.model, using = self._db)
    return query.with_answers_count().with_author().with_tags()

  def newest(self):
    return self.order_by('-pub_date')

  def hottest(self):
    return self.order_by('-likes')

  def by_tag(self, tag):
    return self.filter(tags = tag)

  def single(self, id):
    query = self.queryset()
    return query.with_answers().get(pk = id)

  def week_top(self):
    prev_week = timezone.now() + datetime.timedelta(-7)
    return self.queryset().hottest.with_date_later(prev_week)

#---- Questions manager end ----#

#---- Question model ----#

class Question(models.Model):
  title = models.CharField(max_length = 100)
  text = models.TextField()
  author = models.ForeignKey(User)
  pub_date = models.DateTimeField(default = timezone.now)
  tags = models.ManyToManyField(Tag)
  likes = models.IntegerField(default = 0)

  objects = QuestionManager()

  def get_url(self):
    return reverse('question', kwargs = { 'id' : self.id })

  def correct_answer(self):
    try:
      answer = Answer.objects.get(question = self, correct = True)
    except: 
      answer = None
    return answer

  def __str__(self):
    return "[" + str(self.id) + "] " + self.title

  class Meta:
    ordering = ['-pub_date']

#---- Question model end ----#

#---- Likes ----#

#------ Likes manager ------#

class QuestionLikeManager(models.Manager):
  def has(self, question):
    return self.filter(question = question)

  def sum_for_question(self, question):
    return self.has(question).aggregate(sum = Sum('value'))['sum']

  def add(self, author, question, value):
    if author.id == question.author.id:
      raise QuestionLike.OwnLike
    try:
      like = self.get(author = author, question =question)
    except QuestionLike.DoesNotExist:
      like = self.create(author = author, question = question, value = value)
      question.likes = self.sum_for_question(question)
      question.save()
    else:
      raise QuestionLike.AlreadyLike

  def add_or_update(self, author, question, value):
    like, new = self.update_or_create(author = author, question = question, defaults = { 'value' : value })
    question.likes = self.sum_for_question(question)
    question.save()
    return new

#------ Likes manager end ------#

#------ Like model ------#

class QuestionLike(models.Model):
  class OwnLike(Exception):
    def __init__(self):
      super(QuestionLike.OwnLike, self).__init__(u'Вы не можете голосовать за собственный вопрос')

  class AlreadyLike(Exception):
    def __init__(self):
      super(QuestionLike.AlreadyLike, self).__init__(u'Вы уже оценили этот вопрос')

  LIKE = 1
  DISLIKE = -1

  question = models.ForeignKey(Question)
  author = models.ForeignKey(User)
  value = models.SmallIntegerField(default = LIKE)

  objects = QuestionLikeManager()

  def __str__(self):
    result = "[" + str(self.id) + "] " + self.author.username + " "
    if int(self.value) > 0:
      result += "<3"
    else:
      result += "<||3"
    result +=  " qid" + str(self.question.id)
    return result

#------ Like model end ------#

#---- Likes end ----#

#-- Questions end --#

#-- Answers --#

#---- Queryset ----#

class AnswerQueryset(models.QuerySet):
  def with_author(self):
    return self.select_related('author').select_related('author__userdata')

  def with_question(self):
    return self.select_related('question')

  def hottest(self):
    return self.order_by('-likes')

  def with_date_later(self, date):
    return self.filter(pub_date__gt = date)

#---- Queryset end ----#

#---- Manager ----#

class AnswerManager(models.Manager):
  def queryset(self):
    query = AnswerQueryset(self.model, using = self._db)
    return query.with_author()

  def create(self, **kwargs):
    answer = super(AnswerManager, self).create(**kwargs)
    text = answer.text[:100]
    if len(ans.text) > 100:
      text += '...'
    return answer

  def week_top(self):
    prev_week = timezone.now() + datetime.timedelta(-7)
    return self.queryset().hottest().with_date_later(prev_week)

#---- Manager end ----#

#---- Answer model ----#

class Answer(models.Model):
  text = models.TextField()
  question = models.ForeignKey(Question)
  author = models.ForeignKey(User)
  pub_date = models.DateTimeField(default = timezone.now)
  correct = models.BooleanField(default = False)
  likes = models.IntegerField(default = 0)

  objects = AnswerManager()

  def set_correct(self, user = None):
    question = self.question
    if user is not None and question.author.id != user.id:
      raise Exception(u'Вы не являетесь автором данного вопроса')
    current = question.correct_answer()
    if current is not None:
      current.set_incorrect()
    self.correct = True
    self.save()

  def set_incorrect(self):
    self.correct = False
    self.save()

  def __str__(self):
    "[" + str(self.id) + "] " + self.text

  class Meta:
    ordering = ['-correct', '-pub_date', '-likes']

#---- Answer model end ----#

#---- Likes ----#

#------ Likes manager ------#

class AnswerLikeManager(models.Manager):
  def has(self, answer):
    return self.filter(answer = answer)

  def sum_for_answer(self, answer):
    return self.has(answer).aggregate(sum = Sum('value'))['sum']

  def add(self, author, answer, value):
    if author.id == answer.author.id:
      raise AnswerLike.OwnLike
    try:
      like = self.get(author = author, answer = answer)
    except AnswerLike.DoesNotExist:
      like = self.create(author = author, answer = answer, value = value)
      answer.likes = self.sum_for_answer(answer)
      answer.save()
    else:
      raise AnswerLike.AlreadyLike

  def add_or_update(self, answer, author, value):
    like, new = self.update_or_create(author = author, answer = answer, defaults = { 'value' : value })
    answer.likes =self.sum_for_answer(answer)
    answer.save()
    return new

#------ Likes manager end ------#

#------ Like model ------#

class AnswerLike(models.Model):
  class OwnLike(Exception):
    def __init__(self):
      super(AnswerLike.OwnLike, self).__init__(u'Вы не можете голосовать за собственный ответ')

  class AlreadyLike(Exception):
    def __init__(self):
      super(AnswerLike.AlreadyLike, self).__init__(u'Вы уже оценили этот вопрос')
  
  LIKE = 1
  DISLIKE = -1

  answer = models.ForeignKey(Answer)
  author = models.ForeignKey(User)
  value = models.SmallIntegerField(default = LIKE)

  objects = AnswerLikeManager()

  def __str__(self):
    result = "[" + str(self.id) + "] " + self.author.username + " "
    if int(self.value) > 0:
      result += "<3"
    else:
      result += "<||3"
    result += " aid" + str(self.answer.id)
    return result

#------ Like model end ------#

#---- Likes end ----#

#-- Answers end --#

