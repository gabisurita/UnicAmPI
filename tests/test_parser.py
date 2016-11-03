from __future__ import unicode_literals, absolute_import

import unittest

from unicampi.dac_parser import DacParser


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = DacParser()

    def test_get_institutes(self):
        inst = self.parser.get_institutes()
        self.assertTrue(len(inst) > 0)

    def test_get_subjects(self):
        inst = self.parser.get_subjects('FEEC')
        self.assertTrue(len(inst) > 0)

    def test_get_subjects_ifgw(self):
        inst = self.parser.get_subjects('IFGW')
        self.assertTrue(len(inst) > 0)
        codes = [f['sigla'] for f in inst]
        self.assertIn('F_128', codes)

    def test_get_subject(self):
        inst = self.parser.get_subject('EA611')
        self.assertEquals(inst['nome'], 'Circuitos II')

    def test_get_subject_ifgw(self):
        inst = self.parser.get_subject('F_502')
        self.assertEquals(inst['nome'], 'Eletromagnetismo I')

    def test_get_offerings(self):
        inst = self.parser.get_offerings('MC202', '2016', '1')
        self.assertTrue(len(inst) > 0)

    def test_get_offering(self):
        inst = self.parser.get_offering('MC202', 'A', '2016', '2')
        students = inst.pop('alunos')

        inst_info = {
            "semestre": "2",
            "matriculados": "27",
            "turma": "A",
            "vagas": "25",
            "professor": "Guilherme Pimentel Telles",
            "ano": "2016",
            "sigla": "MC202"
        }

        self.assertEquals(len(students), 27)
        self.assertIn('nome', students[17])
        self.assertIn('ra', students[17])
        self.assertDictContainsSubset(inst, inst_info)
