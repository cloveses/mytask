import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        pass

    @property
    def current_user(self):
        pass

    def write_json(self, obj):
        """Writes the JSON-formated string of the give obj
        to the output buffer"""
        self.set_header('Content-Type', 'application/json')
        from json import dumps
        return self.write(dumps(obj))

    def get_params(self,keys):
        params = dict()
        for key in keys:
            params[key] = self.get_argument(key, strip=True, default='')
        return {k:v for k,v in params.items() if v}

def route(pattern, priority = 0, domain_pattern = None):
    """ Wrap the request handler to do url route
    :param pattern: url pattern
    :param priority: the priority of url pattern
    :param domain_pattern: domain pattern
    """
    def wrap(handler):
        if not issubclass(handler, tornado.web.RequestHandler):
            raise ValueError("must be a subclass of tornado.web.RequestHandler")

        if hasattr(handler, "__routes__"):
            handler.__routes__.append((pattern, priority))
        else:
            handler.__routes__ = [(pattern, priority)]

        handler._domain_pattern = domain_pattern

        return handler
    return wrap