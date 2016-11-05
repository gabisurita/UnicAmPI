# coding:utf-8

"""Views"""

from cornice.resource import resource

from .repositories import (CoursesRepository, EnrollmentsRepository,
                           InstitutesRepository, OfferingsRepository)

ENDPOINTS = {
    'Institutos': {
        'collection_path': '/institutos',
        'path': '/institutos/{id}',
    },
    'Disciplinas': {
        'collection_path': '/institutos/{instituto}/disciplinas',
        'path': '/disciplinas/{id}',
    },
    'Oferecimentos': {
        'collection_path': '/periodos/{periodo}/oferecimentos/{disciplina}',
        'path': '/periodos/{periodo}/oferecimentos/{disciplina}/turma/{id}',
    },
    'Matriculados': {
        'collection_path': '/periodos/{periodo}/oferecimentos/{disciplina}'
                           '/turma/{turma}/matriculados',
        'path': '/periodos/{periodo}/oferecimentos/{disciplina}/turma/{turma}'
                '/matriculados/{id}',
    },
}


class BaseResource(object):
    """Base Resource.

    Base mixin for any cornice resource.

    """

    def __init__(self, request):
        self.request = request
        self._process_request_params()

    @property
    def params(self):
        return self.request.matchdict

    def _process_request_params(self):
        pass


class ModelResource(BaseResource):
    """Model Resource.

    Base class for model resources (i.e., resources that are associated with
    a repository -- a collection of entries).

    """

    repository = None

    def collection_get(self):
        return self.repository().all()

    def get(self):
        try:
            return self.repository().find(self.params['id'])

        except KeyError:
            self.request.errors.add('body', 'id', 'The entry does not exist')
            self.request.errors.status = '404'


@resource(path='/')
class Hello(BaseResource):
    def get(self):
        return {'path': ENDPOINTS}


@resource(**ENDPOINTS['Institutos'])
class Institute(ModelResource):
    repository = InstitutesRepository

    def _process_request_params(self):
        if 'id' in self.params:
            self.params['id'] = self.params['id'].upper()

@resource(**ENDPOINTS['Disciplinas'])
class Courses(ModelResource):
    def repository(self):
        return (CoursesRepository()
                .filter(institute=self.params['instituto']))


@resource(**ENDPOINTS['Oferecimentos'])
class Offering(ModelResource):
    def _process_request_params(self):
        if 'periodo' in self.params:
            self.params['periodo'] = self.params['periodo'].lower()

        if 'disciplina' in self.params:
            self.params['disciplina'] = self.params['disciplina'].upper()

    def repository(self):
        year, term = self.params['periodo'].split('s', 1)

        return (OfferingsRepository()
                .filter(year=year, term=term,
                        course=self.params['disciplina']))


@resource(**ENDPOINTS['Matriculados'])
class Enrollments(ModelResource):
    def _process_request_params(self):
        if 'periodo' in self.params:
            self.params['periodo'] = self.params['periodo'].lower()

        if 'disciplina' in self.params:
            self.params['disciplina'] = self.params['disciplina'].upper()

        if 'turma' in self.params:
            self.params['turma'] = self.params['turma'].lower()

    def repository(self):
        year, term = self.params['periodo'].split('s', 1)

        return (EnrollmentsRepository()
                .filter(year=year, term=term,
                        course=self.params['disciplina'],
                        offering=self.params['turma']))
