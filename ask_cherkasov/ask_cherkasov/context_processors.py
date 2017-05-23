from ask_cherkasov.models import Tag, AppCacher
from django.contrib.auth.models import User

def popular_tags(request):
  tags = AppCacher.get_popular_tags()
  return { 'popular_tags' : tags }

def best_users(request):
  users = AppCacher.get_best_users()
  return { 'best_users' : users }
