"""gnat test suite."""

import unittest

import gnat as g

import numpy as np

R=10.0

class L2(g.Metric):
    
    def dist(self, x, y):
        return np.linalg.norm(x - y)


class L0(g.Metric):
    
    def dist(self, x, y):
        return np.max(np.abs(x - y))

def randomx(m=10, r=R):
    return r * (2 * np.random.random(m) - 1)

class TestDB(object):

    def __init__(self, n=100):
        self.ps = [randomx() for count in xrange(n)]

    def iter_samplekeys(self):
        for key in xrange(len(self.ps)):
            yield key

    def get_sample(self, key):
        return self.ps[key]


def linear_query(db, metric, p, r):
    for key in db.iter_samplekeys():
        q = db.get_sample(key)
        if metric.dist(p, q) < r:
            yield key


def linear_neighbor_query(db, metric, p):

    nn_key = -1e100
    nn_dist = 1e100

    for key in db.iter_samplekeys():
        q = db.get_sample(key)
        d = metric.dist(p, q)
        if d < nn_dist:
            nn_key = key
            nn_dist = d


    return nn_key


class JustMakeGnat(object):
    
    def make_gnat(self, db, metric):
        return g.build_gnat(db, metric=metric)

class QueryTestCase(JustMakeGnat, unittest.TestCase):

    metric=L2()

    def test_search(self):
        metric = self.metric
        db = TestDB()
        gnat = self.make_gnat(db, metric)
        
        r = 0.3 * R
        for count in xrange(20):
            p = randomx()
            
            linear_keys = set(linear_query(db, metric, p, r))

            gnat_keys = set(gnat.query(p, r))

            self.assertEqual(linear_keys, gnat_keys)

class L0QueryTestCase(QueryTestCase):
    metric=L0()


class NearestNeighborTestCase(JustMakeGnat, unittest.TestCase):

    metric=L2()

    def test_neighbor_search(self):
        metric = self.metric
        db = TestDB()
        gnat = g.build_gnat(db, metric=self.metric)
        for count in xrange(20):
            p = randomx()
            
            linear_key = linear_neighbor_query(db, metric, p)

            gnat_key = list(gnat.neighbor_query(p))[0]

            self.assertEqual(linear_key, gnat_key)


class L0NearestNeighborTestCase(NearestNeighborTestCase):

    metric=L0()

class SaveLoadGnat(object):

    def make_gnat(self, db, metric):
        gnat = g.build_gnat(db, metric=metric)

        serialized = g.gnat_table_rows(gnat)

        return g.load_gnat_from_rows(db, serialized, metric)

class SaveLoadQueryTestCase(SaveLoadGnat, QueryTestCase):
    pass

class SaveLoadL0QueryTestCase(SaveLoadGnat, L0QueryTestCase):
    pass


class SaveLoadNearestNeighborTestCase(SaveLoadGnat, NearestNeighborTestCase):
    pass

class SaveLoadL0NearestNeighborTestCase(SaveLoadGnat, L0NearestNeighborTestCase):
    pass

    

if __name__ == "__main__":
    unittest.main()
    
