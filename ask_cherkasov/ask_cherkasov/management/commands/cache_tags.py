from django.core.management.base import BaseCommand, CommandError

from ask_cherkasov.models import AppCacher

class Command(BaseCommand):
  help = 'caches popular tags'

  def handle(self, *args, **kwargs):
    AppCacher.update_popular_tags()
    print('popular tags cached')
