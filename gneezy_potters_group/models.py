from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from gneezy_potters_group.config import *
import random
from random import randrange
from random import random
from statistics import median

author = 'Your name here'

doc = """
Certainty equivalents with BDM. Majority voting rule for the group.
"""


class Subsession(BaseSubsession):

    rand_round = models.IntegerField()

    def creating_session(self):
        self.rand_round = randrange(1, Constants.num_rounds + 1)
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
    winner = models.IntegerField()
    investment = models.FloatField()

    def set_group_payoffs(self, round_num):
        self.random_draw = random()
        if self.random_draw < self.get_player_by_id(1).participant.vars['environment'][round_num - 1][2]:
            self.winner = 1
        else:
            self.winner = 0

        endowment = Constants.endowment[round_num - 1]
        multiplier = Constants.multiplier[round_num - 1]

        self.investment = median([p.participant.vars['investment'][round_num - 1] for p in self.get_players()])

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

