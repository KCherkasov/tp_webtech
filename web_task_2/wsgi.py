from cgi import parse_qs

def application(environ, start_response):
  status = '200 OK'
  endl = "\n";
  urstring = '';
  #rstring = bytes(urstring, 'UTF-8')
  rstring = "<html>\n  <body>\n    <b>Hello world!</b>" + endl + "    <br /><hr />" + endl
  rstring = rstring + "    <h3>REQUEST_METHOD : <b>" + environ['REQUEST_METHOD'] + "</b></h3>\n    <h3><b>GET</b> params:</h3>\n    <br />\n    <ul>"
  query = parse_qs(environ['QUERY_STRING'])
  for p in query:
    rstring += "\n      <li>" + p + " : " + query[p][0] + " ;</li>"
  rstring += endl + "    </ul>\n    <h3><b>POST</b> params:</h3>\n    <br />\n    <ul>\n"
  request_body_size = int(environ.get('CONTENT_LENGTH', 0)) if environ.get('CONTENT_LENGTH') else 0
  rstring += '      <li>CONTENT_LENGTH : ' + str(request_body_size) + " ;</li>"
  request_body = environ['wsgi.input'].read(request_body_size)
  post = parse_qs(request_body)
  for key in post:
    rstring += "\n      <li>" + str(key, 'UTF-8') + " : " + str(post[key][0], 'UTF-8') + " ;</li>"
  #urstring = rstring.decode(encoding='UTF-8')
  rstring += "\n    </ul>\n  </body>\n</html>\n"
  start_response(status, [ ('Content-Type', 'text/html'), ('Content-length', str(len(rstring))) ])
  return [bytes(rstring, 'UTF-8')]
