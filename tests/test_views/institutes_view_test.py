"""Institutes View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import main


class InstituteViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(main({}))

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_collection_get(self):
        response = self.app.get('/institutos', status=200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get(self):
        response = self.app.get('/institutos/IC', status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_lowercase(self):
        response = self.app.get('/institutos/ic', status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_not_found(self):
        self.app.get('/institutos/ICdjjadij', status=404, expect_errors=True)
