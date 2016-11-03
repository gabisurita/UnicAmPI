# coding:utf-8
from cornice.resource import resource

from unicampi import dac_parser

ENDPOINTS = {
    'Institutos': {
        'collection_path': '/institutos',
        'path': '/institutos/{sigla}',
    },
    'Disciplinas': {
        'collection_path': '/institutos/{instituto}/disciplinas',
        'path': '/disciplinas/{sigla}',
    },
    'Oferecimentos': {
        'collection_path': '/periodos/{periodo}/oferecimentos/{sigla}',
        'path': '/periodos/{periodo}/oferecimentos/{sigla}/{turma}',
    },
    'Matriculados': {
        'path': '/periodos/{periodo}/oferecimentos/{sigla}/{turma}/'
                'matriculados',
    },
}


class ApiResource(object):
    def __init__(self, request):
        self.request = request


@resource(path='/')
class Hello(ApiResource):
    def get(self):
        return {'path': ENDPOINTS}


@resource(**ENDPOINTS['Institutos'])
class Institute(ApiResource):
    def __init__(self, request):
        super(Institute, self).__init__(request)
        self.institute_list = dac_parser.get_institutes()

    def collection_get(self):
        return self.institute_list

    def get(self):
        institute = [inst for inst in self.institute_list
                     if inst['sigla'].upper() == self.request.matchdict[
                         'sigla'].upper()]

        if institute:
            return institute[0]
        else:
            raise KeyError


@resource(**ENDPOINTS['Disciplinas'])
class Subject(ApiResource):
    def collection_get(self):
        institute = self.request.matchdict['instituto'].upper()
        return dac_parser.get_subjects(institute)

    def get(self):
        name = self.request.matchdict['sigla'].upper()
        return dac_parser.get_subject(name)


@resource(**ENDPOINTS['Oferecimentos'])
class Offering(ApiResource):
    def __init__(self, request):
        self.request = request
        self.periodo = request.matchdict['periodo'].lower()
        self.ano, self.sem = self.periodo.split('s', 1)

    def collection_get(self):
        data = self.request.matchdict
        return dac_parser.get_offerings(data['sigla'].upper(),
                                        self.ano,
                                        self.sem)

    def get(self):
        data = self.request.matchdict
        self.offering = dac_parser.get_offering(data['sigla'].upper(),
                                                data['turma'].upper(),
                                                self.ano, self.sem)

        self.enrollments = self.offering.pop('alunos', {})

        return self.offering


@resource(**ENDPOINTS['Matriculados'])
class Enrollments(Offering):
    def __init__(self, request):
        self.request = request
        self.periodo = request.matchdict['periodo'].lower()
        self.ano, self.sem = self.periodo.split('s', 1)

    def get(self):
        super(Enrollments, self).get()
        return self.enrollments
