#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from cyrusbus import Bus

class TestBus(unittest.TestCase):
    def callback(self, argument):
        self.has_run = True
        self.argument = argument

    def setUp(self):
        self.bus = Bus()
        self.has_run = False

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
