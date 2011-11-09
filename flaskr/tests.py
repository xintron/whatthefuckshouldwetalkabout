import unittest

from flask import json
from mongoengine import connect

import flaskr
from models import Topic

def _cleanup():
    """Reset indexes, clean all connections cached in the _document_registry.
    Drop databases
    """

    from mongoengine.queryset import QuerySet
    from mongoengine.base import _document_registry

    QuerySet._reset_already_indexed()
    for k, doc in _document_registry.items():
        if not hasattr(doc, '_get_collection'):
            continue
        if doc._meta.get('abstract', False):
            continue
        col = doc._get_collection()
        col.database.connection.drop_database(col.database.name)


class flaskrTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('flaskrtestsuite')
        _cleanup()

    def setUp(self):
        flaskr.app.config['TESTING'] = True
        self.client = flaskr.app.test_client()

    def tearDown(self):
        _cleanup()

    def testGetRandom(self):
        Topic(topic='foolar', ip='127.0.0.1').save()
        Topic(topic='coffee', ip='127.0.0.1').save()
        Topic(topic='tea', ip='127.0.0.1').save()

        r = self.client.get('/api/1/topics/')
        data = json.loads(r.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['data']), 1)

        r = self.client.get('/api/1/topics/?count=2')
        data = json.loads(r.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['data']), 2)

    def testAPIAdd(self):
        topic = 'This is my test topic'
        for i in xrange(2):
            r = self.client.post('/api/1/topics/',
                    data={'topic': topic},
                    environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
            self.assertEqual(r.status, '200 OK') # Should always return 200
            if i == 0:
                self.assertEqual(json.loads(r.data)['success'], True)
            else:
                self.assertEqual(json.loads(r.data)['success'], False)

        r = self.client.post('/api/1/topics/', data={},
                environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
        data = json.loads(r.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'].startswith('[ValidationError]'), True)

    @unittest.skip('not implemented yet')
    def testAPIVote(self):
        Topic(topic='foobar', ip='127.0.0.1').save()
        t = json.loads(self.client.get('/api/1/topics/').data)

        dataset = [(1, '127.0.0.1'),
            (1, '10.0.0.1'),
            (-1, '192.0.0.1')]
        for data in dataset:
            r = self.client.post('/api/1/topics/{}/votes/'.format(
                'up' if data[0] == 1 else 'down'), data={'id': t['data'][0]['id']},
                environ_overrides={'REMOTE_ADDR': data[1]})
            self.assertEqual(json.loads(r.data)['success'], True)

        r = self.client.post('/api/1/votes/down', data={'id': t['data'[0]]['id']},
            environ_overrides={'REMOTE_ADDR': '127.0.0.1'})

if __name__ == '__main__':
    unittest.main()
