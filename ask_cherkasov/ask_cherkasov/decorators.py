from django.contrib.auth import decorators
from ask_cherkasov import mod_ajax

def login_required(func):
  return decorators.login_required(func, redirect_field_name='continue')

def ajax_login_required(func):
  def check(request, *args, **kwargs):
    if request.user.is_authenticated():
      return func(request, *args, **kwargs)
    return mod_ajax.HttpResponseAjaxError(code = 'no_auth', message = 'Необходимо авторизоваться на сайте')
  return check
