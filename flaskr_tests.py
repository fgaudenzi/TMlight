import os
from testmanager.TestManager import app
import unittest
import tempfile
from testmanager.model.user import User

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            app.init_db()

    def tearDown(self):
        pass
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()
        

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Hello World!' in rv.data

if __name__ == '__main__':
    unittest.main()