#!/usr/bin/env python
#-*- coding:utf-8 -*-

class Bus(object):

    def __init__(self):
        self.reset()

    def subscribe(self, key, callback, force=False):
        """
        This method subscribes an function to an eventkey.

        :param key: The event key. When someone published an event with the same key, this subscription will be triggered.
        :param callback: The callback function. This function will be executed when the given event is published.
        :param force: Force insert to execution queue. If True: the callback will be executed, even if the callback is subscribed more than once.
        :return: The busobject.
        """
        if key not in self.subscriptions:
            self.subscriptions[key] = []

        subscription = {
            'key': key,
            'callback': callback
        }

        if force or not self.has_subscription(key, callback):
            self.subscriptions[key].append(subscription)

        return self

    def unsubscribe(self, key, callback):
        """
        This method unsubscribes an function of the given eventkey.

        :param key: The event key.
        :param callback: The callback function.
        """
        if not self.has_subscription(key, callback):
            return self

        self.subscriptions[key].remove({
            'key': key,
            'callback': callback
        })

    def unsubscribe_all(self, key):
        """
        This method unsubscribes all callback functions of the given eventkey.

        :param key: The event key. When someone published an event with the same key, this subscription will be triggered.
        """
        if key not in self.subscriptions:
            return self

        self.subscriptions[key] = []

    def has_subscription(self, key, callback):
        """
        This method shows whether a function has subscriptions or not.

        :param key: The event key.
        :param callback: The callback function.
        :return: True if there is an subscription.
        """
        if key not in self.subscriptions:
            return False

        subscription = {
            'key': key,
            'callback': callback
        }

        return subscription in self.subscriptions[key]

    def has_any_subscriptions(self, key):
        """
        This method shows whether an eventkey has any subscriptions or not.

        :param key: The event key.
        :return: True if there are subscribers.
        """
        return key in self.subscriptions and len(self.subscriptions[key]) > 0

    def publish(self, key, *args, **kwargs):
        """
        Publishes an event. All subscribers to the event will be called.

        :param key: The event key to which the subscriptions should be triggered.
        :param *args: Additional arguments to give the callback functions.
        """
        if not self.has_any_subscriptions(key):
            return self

        for subscriber in self.subscriptions[key]:
            subscriber['callback'](self, *args, **kwargs)

    def reset(self):
        """
        Resets the eventbus. All subscribers will be cleared.
        """
        self.subscriptions = {}