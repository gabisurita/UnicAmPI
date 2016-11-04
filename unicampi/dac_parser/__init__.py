# coding: utf-8
from __future__ import unicode_literals, absolute_import

import requests
from bs4 import BeautifulSoup

from .urls import (PUBLIC_MENU_URL, INSTITUTES_URL, SUBJECTS_URL,
                   OFFERING_URL, OFFERINGS_URL, PERIODS)
from .utils import (ContentFinder, get_current_semester)


class DacParser(object):

    def __init__(self):
        self.session = requests.Session()

    def get_institutes(self, semester=None):

        if not semester:
            year, semester = get_current_semester()
            semester = str(semester)

        page = self.session.get(INSTITUTES_URL.format(period=PERIODS[semester]))

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        # Get 3rd table
        data = tds[3].find_all('td')
        data = [el.text.strip() for el in data]

        codes = data[::2]
        names = data[1::2]

        institutes = [{'sigla': c, 'nome': n} for c, n in zip(codes, names)]

        return institutes

    def get_offerings(self, subject, year=None, semester=None):

        if not semester:
            year, semester = get_current_semester()
            semester = str(semester)
            year = str(year)

        token = self._get_token()
        page = self.session.get(OFFERINGS_URL.format(subject=subject.upper(), year=year,
                                                     semester=semester, token=token))

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        # Get table 8
        data = tds[8]
        data = [lin.find_all('td') for lin in data.find_all('tr')[2:]]

        offs = []
        for line in data:
            offs.append({
                'turma': line[0].text,
                'vagas': line[1].text,
                'matriculados': line[2].text,
            })
        return offs

    def get_offering(self, subject, cls, year, semester):

        token = self._get_token()
        page = self.session.get(OFFERING_URL.format(subject=subject.upper(), cls=cls.upper(),
                                                    year=year, semester=semester, token=token))

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        # Get table 6 (general info)
        data = tds[6]

        finder = ContentFinder(data.text)

        teacher = finder.find_by_content('Docente:').split(':', 1)[1].strip()
        situation = finder.find_by_content('Situação:').split(':', 1)[1].strip()

        # Data is type "Situação:  25 vagas  -  12 matriculados" 
        vacancy, registered = situation.split('-')

        vacancies = vacancy.strip().split(' ', 1)[0]
        registered = registered.strip().split(' ', 1)[0]

        # Get table 8 (students)
        students_data = tds[8].find_all('td')

        # Remove heder
        students_data = [s.text for s in students_data[7:]]

        students = []
        for i in range(0, len(students_data), 6):
            students.append({
                'ra': students_data[i + 1],
                'nome': students_data[i + 2].strip(),
                'curso': students_data[i + 3],
                'tipo': students_data[i + 4],
                'modalidade': students_data[i + 5],
            })

        offering = {
            'sigla': subject,
            'turma': cls,
            'ano': year,
            'semestre': semester,
            'professor': teacher,
            'vagas': vacancies,
            'matriculados': registered,
            'alunos': students
        }

        return offering

    def get_subjects(self, institute, semester=None):

        if not semester:
            year, semester = get_current_semester()
            semester = str(semester)

        session = requests.Session()

        page = session.get(SUBJECTS_URL.format(period=PERIODS[semester], code=institute))

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        data = tds[1].find_all('td')
        # strip and remove raw content
        data = [el.text.strip() for el in data[1:]]

        subjects = []
        for sub in data:
            code = sub[:5]
            name = sub[5:]

            subjects.append({
                'nome': name.strip(),
                'sigla': code.replace(' ', '_'),
            })

        return subjects

    def get_subject(self, code, semester=None):

        if not semester:
            year, semester = get_current_semester()
            semester = str(semester)

        page = self.session.get(SUBJECTS_URL.format(period=PERIODS[semester], code=code))

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        data = tds[1].find_all('td')[1]

        finder = ContentFinder(data.text)

        main_info = finder.splited[0]
        code = main_info[:5]
        name = main_info[5:].strip()

        content = finder.find_by_content('Ementa:', offset=1)
        credits = finder.find_by_content('Créditos:', offset=0)[-3:]
        requires_list = finder.find_by_content('Pré-Requisitos:', offset=1,
                                               end_pattern='Turma:')

        req_dates = requires_list[::2]
        req_values = requires_list[1::2]

        # split 'or' requirements
        req_values = [v.strip().split(' / ') for v in req_values]

        # split 'and' requirements
        for i in range(len(req_values)):
            req_values[i] = [v.strip().split('  ') for v in req_values[i]]

        requires = dict(zip(req_dates, req_values))

        return {
            'nome': name,
            'sigla': code.replace(' ', '_'),
            'ementa': content,
            'pré-requisitos': requires,
            'créditos': int(credits),
        }

    def _get_token(self):
        token_page = self.session.get(PUBLIC_MENU_URL)
        token = token_page.content[1839:1871].decode('ascii')
        return token
