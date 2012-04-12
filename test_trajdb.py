"""trajdb.py test suite."""

import os
import unittest
import itertools as it

import numpy as np

import trajdb


class TempDBCase(object):

    temp_db_name='test.db'
    ndof=10

    def remove_db(self):
        if os.path.exists(self.temp_db_name):
            os.remove(self.temp_db_name)

    def new_db(self):
        return trajdb.open_trajectory_database(self.temp_db_name, ndof=self.ndof, create=True)

    def random_trajectory(self):
        ndof = self.ndof
        while True:
            yield np.random.random(ndof)

    def setUp(self):
        super(TempDBCase, self).setUp()
        self.remove_db()

    def tearDown(self):
        super(TempDBCase, self).tearDown()
        self.remove_db()
            

class AddSamplesTestCase(TempDBCase, unittest.TestCase):

    def test_add_random_trajectory(self):
        db = self.new_db()

        for x in it.islice(self.random_trajectory(), 10):
            db.new_sample(x)


    def test_random_trajectory_samplekeys(self):
        db = self.new_db()

        for x in it.islice(self.random_trajectory(), 10):
            db.new_sample(x)

        samplekeys = list(c for c, in db.select([db.samplekeys.samplekey]))

        self.assertEqual(samplekeys, range(10))


    def test_random_trajectory_trajectories(self):
        db = self.new_db()

        for x in it.islice(self.random_trajectory(), 10):
            db.new_sample(x)

        trajectories = list(c for c, in db.select([db.trajectories.trajectorykey]))

        self.assertEqual(trajectories, [0] * 10)


    def test_random_trajectory_times(self):
        db = self.new_db()

        for x in it.islice(self.random_trajectory(), 10):
            db.new_sample(x)

        times = list(c for c, in db.select([db.times.time]))

        self.assertEqual(times, [0] * 10)


    
        
if __name__ == "__main__":
    unittest.main()
