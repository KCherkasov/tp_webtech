from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from ask_cherkasov.models import Question

from random import choice, randint

import os

class Command(BaseCommand):
  help = 'Creates fake questions'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'Number of questions to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    
    users = User.objects.all()[1:]

    for i in range(0, count):
      question = Question()
      question.author = choice(users)
      question.title = u'Some question number ' + str(i)
      question.text = u'Autogenerated question from user ' + question.author.first_name + ' ' + question.author.last_name
      question.save()
      self.stdout.write('[%d] question added' % (question.id))
      
