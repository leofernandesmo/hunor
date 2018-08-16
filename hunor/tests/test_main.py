from unittest import TestCase
from hunor import main


class TestMain(TestCase):

    def test_hello_world(self):
        self.assertEqual(main.main(), "Hello World!!!")
