# -*- coding: utf-8 -*-

class MasterSlaveRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ('contenttypes', 'sites'):
            return 'default'
        else:
            return 'slave'
    def db_for_write(self, model, **hints):
        return 'default'
