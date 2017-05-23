# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.hashers import make_password
from ask_cherkasov.models import UserData, Question, Tag

import urllib
from django.core.files import File

#-- login form --#

class Sign_in(forms.Form):
  login = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите логин', }), max_length = 30, label = 'Логин')
  password = forms.CharField(widget = forms.PasswordInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите пароль', }), label = 'Пароль')

  def clean(self):
    data = self.cleaned_data
    user = authenticate(username = data.get('login'), password = data.get('password'))
    if user is not None:
      if user.is_active:
        data['user'] = user
      else:
        raise forms.ValidationError('Учетная запись не активна')
    else:
      raise forms.ValidationError('Неверный логин и/или пароль')

#-- login form end --#

#-- signup form --#

class Sign_up(forms.Form):
  username = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите логин', }), max_length = 30, label = 'Логин')
  first_name = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Имя', }), max_length = 30, label = 'Имя')
  last_name = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Фамилия', }), max_length = 30, label = 'Фамилия')
  email = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите e-mail', }), max_length = 30, label = 'Электронная почта')
  password1 = forms.CharField(widget = forms.PasswordInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите пароль', }), min_length = 6, label = 'Пароль')
  password2 = forms.CharField(widget = forms.PasswordInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Подтвердите пароль', }), min_length = 6, label = 'Пароль еще раз')
  about = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Расскажите о себе', }), label = 'О себе')
  avatar = forms.FileField(widget = forms.TextInput(attrs = { 'class' : 'sign-up-form-userpic-input', }), required = False, label = 'Аватар')

  def clean_username(self):
    username = self.cleaned_data.get('username', '')
    try:
      user = User.objects.get(username = username)
      raise forms.ValidationError('Учетная запись с таким названием уже существует')
    except User.DoesNotExist:
      return username

  def clean_password2(self):
    password = self.cleaned_data.get('password1', '')
    confirm = self.cleaned_data.get('password2', '')
    if password != confirm:
      forms.ValidationError('Введенные пароли не совпадают')

  def save(self):
    data = self.cleaned_data
    password = data.get('password1')
    user = User()
    user.username = data.get('username')
    user.password = make_password(password)
    user.email = data.get('email')
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.is_active = True
    user.is_superuser = False
    user.save()
    user_data = UserData()
    user_data.user = user
    user_data.about = data.get('about')
    if data.get('avatar') is not None:
      avatar = data.get('avatar')
      user_data.avatar.save('%s_%s' % (user.username, avatar.name), avatar, save = True)
    user_data.save()
    return authenticate(username = user.username, password = password)

#-- signup form end --#

#-- profile edit form --#

class ProfileEdit(forms.Form):
  first_name = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Имя', }), max_length = 30, label = 'Имя')
  last_name = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Фамилия', }), max_length = 30, label = 'Фамилия')
  email = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите e-mail', }), max_length = 30, label = 'Электронная почта')
  password1 = forms.CharField(widget = forms.PasswordInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Введите пароль', }), min_length = 6, label = 'Пароль')
  password2 = forms.CharField(widget = forms.PasswordInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Подтвердите пароль', }), min_length = 6, label = 'Пароль еще раз')
  about = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Расскажите о себе', }), label = 'О себе')
  avatar = forms.FileField(widget = forms.TextInput(attrs = { 'class' : 'sign-up-form-userpic-input', }), required = False, label = 'Аватар')

  def clean_password2(self):
    password = self.cleaned_data.get('password1', '')
    confirm = self.cleaned_data.get('password2', '')
    if password != confirm:
      forms.ValidationError('Введенные пароли не совпадают')

  def save(self, user):
    data = self.cleaned_data
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    password = self.cleaned_data.get('password1', '')
    if password != '':
      user.set_password(password)
    user.save()
    user_data = user.userdata
    user_data.about = data.get('about')
    if data.get('avatar') is not None:
      avatar = data.get('avatar')
      user_data.avatar.save('%s_%s' % (user.username, avatar.name), avatar, save = True)
    user_data.save()
    return self

#-- profile edit form end --#

#-- answer form --#

class AnswerForm(forms.Form):
  text = forms.CharField(widget = forms.Textarea(attrs = { 'class' : 'form-control', 'rows' : '3', 'placeholder' : 'Ваш ответ...', }))

  def save(self, question, author):
    data = self.cleaned_data
    return question.answer_set.create(text = data.get('text'), author = author)

#-- answer form end --#

#-- question form --#

class QuestionForm(forms.Form):
  title = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Заголовок вопроса', }), max_length = 100, label = 'Тема')
  text = forms.CharField(widget = forms.Textarea(attrs = { 'class' : 'form-control', 'placeholder' : 'Текст', }), label = 'Текст')
  tag1 = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Тег 1', }), required = False)
  tag2 = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Тег 2', }), required = False)
  tag3 = forms.CharField(widget = forms.TextInput(attrs = { 'class' : 'form-control', 'placeholder' : 'Тег 3', }), required = False)

  def save(self, author):
    data = self.cleaned_data
    question = Question.objects.create(title = data.get('title'), text = data.get('text'), author = author)
    question.save()
    for tag_no in ['tag1', 'tag2', 'tag3']:
      tag_text = data.get(tag_no)
      if tag_text is not None and tag_text != '':
        tag = Tag.objects.get_or_create(tag = tag_text)
        question.tags.add(tag)
    return question


#-- question form end --#
