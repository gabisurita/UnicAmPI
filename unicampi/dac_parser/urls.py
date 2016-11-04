# coding: utf-8
from __future__ import unicode_literals


PERIODS = {
    '1': 'G1S0',
    '1e1': 'G1S1',
    '1e2': 'G1S2',
    '1r': 'G5A3',
    '2': 'G2S0',
    '2e1': 'G2S1',
    '2e2': 'G2S2',
    '2r': 'G6A3',
    'fv': 'G5A0',
}

DAC_URL = "http://www.dac.unicamp.br/"

PUBLIC_MENU_URL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'

INSTITUTES_URL = ('http://www.dac.unicamp.br/sistemas/horarios/grad/{period}/'
                  'indiceP.htm')

SUBJECTS_URL = 'http://www.dac.unicamp.br/sistemas/horarios/grad/{period}/{code}.htm'

OFFERINGS_URL = ('http://www.daconline.unicamp.br/altmatr/conspub_situacaovagas'
                 'pordisciplina.do?org.apache.struts.taglib.html.TOKEN={token}&'
                 'cboSubG={semester}&cboSubP=0&cboAno={year}&txtDisciplina={subject}'
                 '&txtTurma=a&btnAcao=Continuar')

OFFERING_URL = ('http://www.daconline.unicamp.br/altmatr/conspub_matriculados'
                'pordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN={token}&'
                'cboSubG={semester}&cboSubP=0&cboAno={year}&txtDisciplina={subject}&'
                'txtTurma={cls}&btnAcao=Continuar')
