from webtest import TestApp
import unittest

from unicampi import main, views


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main({}))

    def test_hello(self):
        resp = self.app.get('/', status=200)
        self.assertEquals(views.ENDPOINTS, resp.json['path'])

    def test_institutes(self):
        resp = self.app.get('/institutos')
        self.assertGreater(len(resp.json), 3)
        fenf = {"sigla": "FENF", "nome": "Faculdade de Enfermagem"}
        self.assertIn(fenf, resp.json)

    def test_subjects(self):
        resp = self.app.get('/institutos/feec/disciplinas')
        self.assertGreater(len(resp.json), 3)
        fenf = {"sigla": "FENF", "nome": "Faculdade de Enfermagem"}
        self.assertIn(fenf, resp.json)
