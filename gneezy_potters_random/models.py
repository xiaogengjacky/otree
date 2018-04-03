
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from gneezy_potters_random.config import *
import random
from random import randrange
from random import random
from statistics import median

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
    random_draw = models.FloatField()
    random_round = models.IntegerField()
    winner = models.IntegerField()
    investment = models.FloatField()
    selection = models.IntegerField()

    def set_group_payoffs(self):
        self.random_round = randrange(1, Constants.num_rounds + 1)

        self.random_draw = random()
        if self.random_draw < self.get_player_by_id(1).participant.vars['environment'][self.random_round - 1][2]:
            self.winner = 1
        else:
            self.winner = 0

        endowment = Constants.endowment[self.random_round - 1]
        multiplier = Constants.multiplier[self.random_round - 1]

        dd = random()
        for k in range(0, Constants.players_per_group):
            if Constants.cum_weight[k] < dd < Constants.cum_weight[k + 1]:
                self.investment = self.get_player_by_id(k+1).participant.vars['investment'][self.random_round - 1]
                self.selection = k + 1

        for p in self.get_players():
            p.payoff = (endowment - self.investment + self.winner * self.investment * multiplier)*(1/3)
            p.participant.vars['payoff'] = p.payoff


class Player(BasePlayer):

    investment = models.CurrencyField(
        min=0, max=Constants.endowment[0],
        doc="""The amount invested by the subject""",
    )

    def set_participant_investment(self, round_num):
        self.participant.vars['investment'][round_num - 1] = self.investment







