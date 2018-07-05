from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Page1(Page):
    form_model = 'player'
    form_fields = ['q1',
                   'q3',
                   'q5']


class Page4(Page):
    form_model = 'player'
    form_fields = ['q11',
                   'q6',
                   'q8']


class Page2(Page):
    form_model = 'player'
    form_fields = ['q4',
                   'q2']


class Page3(Page):
    form_model = 'player'
    form_fields = ['q7',
                   'q12']


page_sequence = [
    Page1,
    Page2,
    Page3,
    Page4
    # CognitiveReflectionTest
]



