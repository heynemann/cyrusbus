#!/usr/bin/env python
#-*- coding:utf-8 -*-

class Bus(object):

    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, key, callback, force=False):
        if key not in self.subscriptions:
            self.subscriptions[key] = []

        subscription = {
            'key': key,
            'callback': callback
        }

        if force or (not subscription in self.subscriptions[key]):
            self.subscriptions[key].append(subscription)

        return self

    def unsubscribe(self, key, callback):
        if key not in self.subscriptions:
            return self

        subscription = {
            'key': key,
            'callback': callback
        }

        if subscription not in self.subscriptions[key]:
            return self

        self.subscriptions[key].remove(subscription)

    def unsubscribe_all(self, key):
        if key not in self.subscriptions:
            return self

        self.subscriptions[key] = []
