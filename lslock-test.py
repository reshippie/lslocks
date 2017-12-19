#! /usr/bin/env

import fcntl
import os
import subprocess
import time
import unittest


class TestLocks(unittest.TestCase):
    tmpdir = '/tmp/lslock-test/'
    locks = [tmpdir + 'sleep.lock', tmpdir + 'other.lock']

    def setUp(self):
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)
        self.all_locks = self.make_locks()

    def tearDown(self):
        for l in self.locks:
            os.remove(l)
        os.rmdir(self.tmpdir)

    def test_negative(self):
        self.assertNotIn(self.tmpdir + 'lock', self.all_locks)

    def test_positive(self):
        for l in self.locks:
            self.assertIn(l, self.all_locks)

    def make_locks(self):
        s0 = subprocess.Popen(['/usr/bin/flock', '-s', self.locks[0], 'sleep', '5'])
        s1 = subprocess.Popen(['/usr/bin/flock', '-s', self.locks[1], 'sleep', '5'])
        lock = open(self.locks[0])
        fcntl.lockf(lock, fcntl.LOCK_SH)
        s2 = subprocess.Popen(['python', 'lslock.py', self.tmpdir], stdout=subprocess.PIPE)
        (out, err) = s2.communicate()
        return out.split()


suite = unittest.TestLoader().loadTestsFromTestCase(TestLocks)
unittest.TextTestRunner(verbosity=2).run(suite)

