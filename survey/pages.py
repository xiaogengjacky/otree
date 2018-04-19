from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'major',
                   'race',
                   'year',
                   'familysize',
                   'familyincome',
                   'personalspending',
                   'volunteer']


# class CognitiveReflectionTest(Page):
#     form_model = 'player'
#     form_fields = ['crt_bat',
#                    'crt_widget',
#                    'crt_lake']

class SubjectiveAttitude(Page):
    form_model = 'player'
    form_fields = ['sa_1',
                   'sa_2',
                   'sa_3',
                   'sa_4']

class GroupAttitude(Page):
    form_model = 'player'
    form_fields = ['sa_5',
                   'sa_6',
                   'sa_7',
                   'sa_8']

page_sequence = [
    Demographics,
    SubjectiveAttitude
    # CognitiveReflectionTest
]


page_sequence.append(GroupAttitude)
