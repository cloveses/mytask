#!/usr/bin/env python
""" Load all handlers and route them which wraped by ~common.web.route decorator.
Import this in your project, use like this::
    from tornado.web import Application
    from common.url import load_handlers
    _handlers, _domain_handlers = load_handlers(["hander.package"])
    app = Application(handlers, **{})
    for (host_pattern, handlers) in _domain_handlers:
        app.add_handlers(host_pattern, handlers)
    ...
"""
import os
import inspect

from .web import BaseHandler


def get_real_obj(obj, pkg):
    """ Import module and get the real module object
    :param obj:   object returned from __import__ function
    :param pkg:   package object returned from __import__ function
    :rtype: Packge or Module Object
    """
    subs = pkg.split(".")
    if len(subs) == 1:
        return obj

    for s in subs[1:]:
        obj = obj.__dict__[s]

    return obj


def get_package_path(pkg):
    """ Return the abs path of package
    :param pkg: Package's name
    :rtype: str
    """
    try:
        pkg_obj = __import__(pkg)
    except ImportError:
        return None

    pkg_obj = get_real_obj(pkg_obj, pkg)
    return os.path.abspath(os.path.dirname(pkg_obj.__file__))


def get_handler_modules(handler_package):
    """ Load all modules from handler package
    :param handler_package: The package name of handlers
    """
    modules = []
    path = get_package_path(handler_package)
    for m in os.listdir(path):
        # print('all .py files.....',m)
        if not m.startswith("_") and (m.endswith(".py") or m.endswith(".pyc")):
            modules.append(handler_package + "." + m.split(".")[0])
    # print("handler_package......",handler_package)
    # print("modules......",modules)
    return modules


def load_handlers(handler_packages):
    """ Load request handler from handler packages
    :param handler_packages: Packages of handlers
    :type handler_packages: list or tuple
    :rtype: (handlers, domainHandlers)
    """
    if isinstance(handler_packages, (str, bytes)):
        handler_packages = [handler_packages]

    assert isinstance(handler_packages, (tuple, list, set, iter))

    # print("handler_packages.....",handler_packages)

    handlers = []
    domain_handlers = []
    for handler_package in handler_packages:
        for module in get_handler_modules(handler_package):
            mobj = get_real_obj(__import__(module), module)

            for key, member in mobj.__dict__.items():
                if inspect.isclass(member) and issubclass(member, BaseHandler)\
                and hasattr(member, "__routes__"):
                    for pattern, priority in member.__routes__:
                        item = (pattern, priority, member)
                        if member._domain_pattern:
                            domain_handlers.append((member._domain_pattern, item))
                        else:
                            handlers.append(item)
    handlers = sorted(handlers, key = lambda x: x[1], reverse = True)
    domain_handlers = sorted(domain_handlers, key = lambda x: x[1][1], reverse = True)

    remove_priority = lambda x: (x[0], x[2])
    remove_domain_priority = lambda x:(x[0], (x[1][0], x[1][2]))
    return (list(map(remove_priority, handlers)),
        list(map(remove_domain_priority, domain_handlers)))