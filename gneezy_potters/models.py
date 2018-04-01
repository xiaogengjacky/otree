
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from gneezy_potters.config import *
import random
from random import randrange
from random import random

author = 'Your name here'

doc = """
Gneezy Potters method to elicit risk preference as in their 1995 QJE paper.
"""


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():

                round_list = (j for j in range(1, Constants.num_rounds+1))
                probabilities = Constants.probability
                multipliers = Constants.multiplier
                endowments = Constants.endowment

                p.participant.vars['environment'] = list(zip(round_list, endowments, probabilities, multipliers))
                p.participant.vars['investment'] = [None for j in range(0, Constants.num_rounds)]
                p.participant.vars['payoff'] = [None for j in range(0, Constants.num_rounds)]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    random_draw = models.FloatField()
    winner = models.IntegerField()
    investment = models.CurrencyField(
        min=0, max=Constants.endowment[0],
        doc="""The amount invested by the subject""",
    )

    def set_payoffs(self, round_num):
        self.random_draw = random()
        if self.random_draw < self.participant.vars['environment'][round_num-1][2]:
            self.winner = 1
        else:
            self.winner = 0

        self.payoff = self.participant.vars['environment'][round_num - 1][1] - self.investment + self.winner * \
            self.investment * self.participant.vars['environment'][round_num - 1][3]

        self.participant.vars['investment'][round_num - 1] = self.investment
        self.participant.vars['payoff'][round_num - 1] = self.payoff







