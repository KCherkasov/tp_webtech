from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask_cherkasov.models import UserData

from django.core.files import File

class Command(BaseCommand):
  help = 'creates fake users'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    for i in range(0, count):
      user = User()
      user.save()
      user.username = 'Bot_' + str(user.id)
      user.first_name = 'Testbot_' + str(user.id % 19)
      user.last_name = 'Fakeuser_' + str(user.id % 23)
      user.email = 'botmail_' + str(i) + '@mail.ru'
      user.password = make_password('Imabot')
      user.is_active = True
      user.is_superuser = False
      user.save()

      user_data = UserData()
      user_data.user = user
      user_data.about = 'Bot user created via management command'

      user_data.save()

      self.stdout.write('[%d] added user %s' % (user.id, user.username))
