from unittest import TestCase

from pyplay.log_book import LogBookRecord, LogMessage, LogMessageFinder, LogBook
from pyplay.name import Name


class MessageA(LogMessage):
    pass


class MessageB(LogMessage):
    pass


class TestLogBookFinder(TestCase):
    def test_by_type(self):
        log_book = LogBook(actor_name='Timber', records=[])
        a = MessageA()
        b = MessageB()

        log_book = LogMessageFinder(
            [
                LogBookRecord(actor=Name('Timber'), message=a),
                LogBookRecord(actor=Name('Timber'), message=b),
            ]
        )
        self.assertEqual(log_book.by_type(MessageB).one(), b)

    def test_by_actor(self):
        a = MessageA()
        b = MessageB()
        log_book = LogMessageFinder(
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
        log_book = LogMessageFinder(records)
        self.assertEqual(
            list(log_book),
            records
        )

    def test_one(self):
        a = MessageA()
        records = [
            LogBookRecord(actor=Name('Piet'), message=a)
        ]
        log_book = LogMessageFinder(records)
        self.assertEqual(log_book.one(), a)

    def test_first(self):
        a = MessageA()
        b = MessageB()
        records = [
            LogBookRecord(actor=Name('Piet'), message=a),
            LogBookRecord(actor=Name('Piet'), message=b)
        ]
        log_book = LogMessageFinder(records)
        self.assertEqual(log_book.first(), a)

    def test_last(self):
        a = MessageA()
        b = MessageB()
        records = [
            LogBookRecord(actor=Name('Piet'), message=a),
            LogBookRecord(actor=Name('Piet'), message=b)
        ]
        log_book = LogMessageFinder(records)
        self.assertEqual(log_book.last(), b)

    def test_one_fails(self):
        a = MessageA()
        b = MessageB()
        records = [
            LogBookRecord(actor=Name('Piet'), message=a),
            LogBookRecord(actor=Name('Timber'), message=b),
        ]
        log_book = LogMessageFinder(records)
        with self.assertRaises(Exception):
            log_book.one()
