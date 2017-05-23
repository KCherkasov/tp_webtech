from django.core.management.base import BaseCommand, CommandError

from ask_cherkasov.models import AppCacher

class Command(BaseCommand):
  help = 'caches current best users'

  def handle(self, *args, **kwargs):
    AppCacher.update_best_users()
    print('best users cached')
