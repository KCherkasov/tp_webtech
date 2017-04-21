from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from ask_cherkasov.models import Question, Answer

from random import choice, randint

import os

class Command(BaseCommand):
  help = 'Fill database with questions'
  def add_arguments(self, parser):
    parser.add_argument('--min', action = 'store', dest = 'min_answers', default = 5, help = 'Minimal number of answers per question')
    parser.add_argument('--max', action = 'store', dest = 'max_answers', default = 15, help = 'Maximal number of answers per question')

  def handle(self, *args, **options):
    min_number = int(options['min_answers'])
    max_number = int(options['max_answers'])

    users = User.objects.all()[1:]
    questions = Question.objects.all()

    for question in questions:
      for i in range(0, min(min_number, max_number)):
        answer = Answer()
        answer.author = choice(users)
        answer.text = 'Answer on question ' + question.title + ' from user ' + question.author.first_name + ' ' + question.author.last_name + ', by user ' + answer.author.first_name + ' ' + answer.author.last_name
        answer.question = question
        answer.save()
        self.stdout.write('[%d] answer on question [%d]' % (answer.id, question.id))

