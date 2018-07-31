#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import settings
from tornado import web, httpserver, ioloop
from tweb.url_map import load_handlers
from tweb.tools import init_secrity_qstn
import tornado.wsgi

init_secrity_qstn()
handlers,domain_handlers = load_handlers(settings.HDL_DIR)


application = tornado.wsgi.WSGIApplication(handlers, **settings.web_server)
for (host_pattern, handlers) in domain_handlers:
    application.add_handlers(host_pattern, handlers)

#http_server = httpserver.HTTPServer(application, xheaders=True)

#port = int(sys.argv[1]) if len(sys.argv) > 1 else settings.port

#http_server.listen(port)
#print()
#print('Server is starting...')
#print('Server\'s port:',port)

# if __name__ == '__main__':
#     ioloop.IOLoop.instance().start()