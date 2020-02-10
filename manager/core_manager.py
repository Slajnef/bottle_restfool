from abc import ABC, abstractmethod
from pydoc import locate

from bottle import Bottle, run

from manager.baseapp import BaseApp
from settings import default_address, apps


def get_default_address():
    _default = default_address
    return _default


def execute_from_command_line(argv):
    try:
        _address = get_default_address()
        if argv.__len__() > 1:
            arg_address = argv[1].split(':')
            _address['host'] = arg_address[0]
            _address['port'] = arg_address[1]
    except Exception as e:
        raise ValueError('wrong address')
    return _address


def get_subclasses(cls):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


class Core(object):
    def __init__(self, address):
        core = Bottle()
        self.register_routers(core)
        run(core, host=address['host'], port=address['port'])

    @staticmethod
    def initialize_baseapps():
        for app in apps:
            baseapp_class = locate(app)
            instance = baseapp_class()

    def register_routers(self, core):
        self.initialize_baseapps()
        base_app_subclasses = get_subclasses(BaseApp)
        for sub_class in base_app_subclasses:
            sub_class.call_router(sub_class, core=core)