from unittest import TestCase

from pyplay.log_book import LogBook, LogBookRecord, LogMessage
from pyplay.name import Name


class MessageA(LogMessage):
    pass


class MessageB(LogMessage):
    pass


class TestLogBook(TestCase):
    def test_by_type(self):
        a = MessageA()
        b = MessageB()
        log_book = LogBook(
            [
                LogBookRecord(actor=Name('Timber'), message=a),
                LogBookRecord(actor=Name('Timber'), message=b),
            ]
        )
        self.assertEqual(log_book.by_type(MessageB).one(), b)

    def test_by_actor(self):
        a = MessageA()
        b = MessageB()
        log_book = LogBook(
            [
                LogBookRecord(actor=Name('Piet'), message=a),
                LogBookRecord(actor=Name('Timber'), message=b),
            ]
        )
        self.assertEqual(log_book.by_actor('Piet').one(), a)

    def test_iteration(self):
        a = MessageA()
        b = MessageB()
        records = [
            LogBookRecord(actor=Name('Piet'), message=a),
            LogBookRecord(actor=Name('Timber'), message=b),
        ]
        log_book = LogBook(records)
        self.assertEqual(
            list(log_book),
            records
        )

    def test_one_fails(self):
        a = MessageA()
        b = MessageB()
        records = [
            LogBookRecord(actor=Name('Piet'), message=a),
            LogBookRecord(actor=Name('Timber'), message=b),
        ]
        log_book = LogBook(records)
        with self.assertRaises(Exception):
            log_book.one()
