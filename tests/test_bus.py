#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from cyrusbus import Bus

class TestBus(unittest.TestCase):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.has_run = True
        self.argument = argument

    def setUp(self):
        self.bus = Bus()
        self.has_run = False
        self.called_bus = None

    def test_can_haz_bus(self):
        assert self.bus

    def test_has_no_subscriptions(self):
        assert not self.bus.subscriptions

    def test_subscribe_is_chainable(self):
        bus = self.bus.subscribe('test.key', self.callback)
        assert bus == self.bus

    def test_can_subscribe_to_event(self):
        self.bus.subscribe('test.key', self.callback)
        expected = [{ 'key': 'test.key', 'callback': self.callback }]

        assert 'test.key' in self.bus.subscriptions
        assert self.bus.subscriptions['test.key']
        assert expected == self.bus.subscriptions['test.key']

    def test_subscribing_twice_with_same_subject_and_callback_ignores_second_call(self):
        self.bus.subscribe('test.key', self.callback).subscribe('test.key', self.callback)

        assert len(self.bus.subscriptions['test.key']) == 1, len(self.bus.subscriptions['test.key'])

    def test_subscribing_by_force(self):
        self.bus.subscribe('test.key', self.callback).subscribe('test.key', self.callback, force=True)

        assert len(self.bus.subscriptions['test.key']) == 2, len(self.bus.subscriptions['test.key'])

    def test_unsubscribe_is_chainable(self):
        bus = self.bus.unsubscribe('test.key', self.callback)
        assert bus == self.bus

    def test_unsubscribe_to_invalid_subject_does_nothing(self):
        self.bus.unsubscribe('test.key', self.callback)

        assert 'test.key' not in self.bus.subscriptions

    def test_unsubscribe_to_invalid_callback_does_nothing(self):
        self.bus.subscribe('test.key', self.callback)
        self.bus.unsubscribe('test.key', lambda obj: obj)

        assert len(self.bus.subscriptions['test.key']) == 1, len(self.bus.subscriptions['test.key'])

    def test_can_unsubscribe_to_event(self):
        self.bus.subscribe('test.key', self.callback).unsubscribe('test.key', self.callback)

        assert len(self.bus.subscriptions['test.key']) == 0, len(self.bus.subscriptions['test.key'])

    def test_unsubscribe_all_does_nothing_for_nonexistent_key(self):
        self.bus.subscribe('test.key', self.callback)
        self.bus.unsubscribe_all('other.key')

        assert len(self.bus.subscriptions['test.key']) == 1, len(self.bus.subscriptions['test.key'])

    def test_unsubscribe_all_is_chainable(self):
        bus = self.bus.unsubscribe_all('test.key')
        assert bus == self.bus

    def test_unsubscribe_all(self):
        self.bus.subscribe('test.key', self.callback)
        self.bus.subscribe('test.key', lambda obj: obj)

        self.bus.unsubscribe_all('test.key')

        assert len(self.bus.subscriptions['test.key']) == 0, len(self.bus.subscriptions['test.key'])

    def test_has_subscription(self):
        self.bus.subscribe('test.key', self.callback)

        assert self.bus.has_subscription('test.key', self.callback)

        self.bus.unsubscribe('test.key', self.callback)

        assert not self.bus.has_subscription('test.key', self.callback)

    def test_does_not_have_subscription_for_invalid_key(self):
        assert not self.bus.has_subscription('test.key', self.callback)

    def test_does_not_have_subscription_for_invalid_calback(self):
        self.bus.subscribe('test.key', self.callback)

        assert not self.bus.has_subscription('test.key', lambda obj: obj)

    def test_has_any_subscriptions_for_invalid_key(self):
        assert not self.bus.has_any_subscriptions('test.key')

    def test_has_any_subscriptions(self):
        self.bus.subscribe('test.key', self.callback)

        assert self.bus.has_any_subscriptions('test.key')

        self.bus.unsubscribe('test.key', self.callback)

        assert not self.bus.has_any_subscriptions('test.key')

    def test_can_publish(self):
        self.bus.subscribe('test.key', self.callback)

        self.bus.publish('test.key', argument="something")

        assert self.has_run
        assert self.argument == "something"
        assert self.called_bus == self.bus

    def test_can_publish_with_noone_listening(self):
        self.bus.publish('test.key', something="whatever")

    def test_publish_is_chainable(self):
        bus = self.bus.publish('test.key', something="whatever")
        assert bus == self.bus

    def test_subscribing_to_different_keys(self):
        self.bus.subscribe('test.key', self.callback)
        self.bus.subscribe('test.key2', self.callback)
        self.bus.subscribe('test.key3', self.callback)

        assert 'test.key' in self.bus.subscriptions
        assert 'test.key2' in self.bus.subscriptions
        assert 'test.key3' in self.bus.subscriptions

        assert self.bus.subscriptions['test.key']
        assert self.bus.subscriptions['test.key2']
        assert self.bus.subscriptions['test.key3']

    def test_can_reset_bus(self):
        self.bus.subscribe('test.key', self.callback)
        self.bus.subscribe('test.key2', self.callback)
        self.bus.subscribe('test.key3', self.callback)

        self.bus.reset()

        assert 'test.key' not in self.bus.subscriptions
        assert 'test.key2' not in self.bus.subscriptions
        assert 'test.key3' not in self.bus.subscriptions
