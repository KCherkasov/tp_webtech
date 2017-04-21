from django.core.management.base import BaseCommand, CommandError

from ask_cherkasov.models import Question, Tag

from random import choice, randint

import os

class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 3, help = 'Number of tags per question')
    parser.add_argument('-r', action = 'store', dest = 'refresh', default = 1, help = 'Refresh questions tags')

  def handle(self, *args, **options):
    tags = ['javascript', 'java', 'objective-C', 'python', 'django', 'gunicorn', 'nginx', 'CSS3', 'C++', 'HTML5', 'bootstrap', 'ubuntu', 'linux', 'SQL', 'SQLite', 'MySQL', 'IOS', 'Windows', 'Node', 'Angular']
    db_tags = Tag.objects.all()
    db_tags.delete()

    colors = Tag.COLORS
    
    for tag in tags:
      obj_tag = Tag()
      obj_tag.tag = tag
      obj_tag.color = choice(colors)[0]
      obj_tag.save()

    count = int(options['count'])
    refresh = int(options['refresh'])
    db_tags = Tag.objects.all()
    if refresh > 0:
      for question in Question.objects.all():
        self.stdout.write('[%d] question' % (question.id))
        for i in range(0, count):
          tag = choice(db_tags)
          if tag not in question.tags.all():
            question.tags.add(tag)

