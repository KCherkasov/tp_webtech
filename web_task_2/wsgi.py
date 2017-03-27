def application(environ, start_response):
  status = '200 OK'
  endl = '\n';
  rstring = 'Hello world!' + endl
  rstring = rstring + 'REQUEST_METHOD : ' + environ['REQUEST_METHOD'] + endl
  query = split_query(environ['QUERY_STRING'])
  if query != '' : 
    rstring = rstring + query + endl
  if environ['REQUEST_METHOD'] == 'POST' :
    try :
      rstring = rstring + 'CONTENT_TYPE : ' + environ['CONTENT_TYPE'] + endl
      rstring = rstring + 'CONTENT_LENGTH : ' + environ['CONTENT_LENGTH'] + endl
      rstring = rstring + 'wsgi.input : ' + environ['wsgi.input'] + endl
    except KeyError:
      rstring = rstring + 'CONTENT_TYPE : ' + endl
      rstring = rstring + 'CONTENT_LENGTH : ' + endl
      rstring = rstring + 'wsgi.input : ' + str(environ['wsgi.input']) + endl
  start_response(status, [ ("Content-Type", "text/plain"), ("Content-Length", str(len(rstring))), ])
  return [rstring.encode('utf-8'), ]

def split_query(qstring):
  params = qstring.split('&')
  if params == [] :
    return ''
  result = '\n'
  result = result.join(params)
  return result
