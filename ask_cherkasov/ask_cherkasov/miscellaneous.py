from django.http import HttpResponse

def paginate(objects, request, key=''):
  from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

  key = key + '_page'

  page = request.GET.get(key)
  paginator = Paginator(objects, 8)

  try:
    result = paginator.page(page)
  except EmptyPage:
    result = paginator.page(1)
  except PageNotAnInteger:
    result = paginator.page(1)

  result.from_left = result.number - 4
  result.from_right = result.number + 4
  result.key = key

  return result
