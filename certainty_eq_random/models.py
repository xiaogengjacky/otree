from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from certainty_eq_random.config import *
import random as rrandom
from random import *
from statistics import median

author = 'JUBO YAN--NTU Econ'

doc = """
Certainty equivalents with BDM. Random selection rule for group.
"""


class Subsession(BaseSubsession):
    chosen_rnd_round = models.IntegerField()

    def creating_session(self):
        self.chosen_rnd_round = randrange(1, Constants.num_rounds + 1)
        if self.round_number == 1:
            for p in self.get_players():

                round_list = (j for j in range(1, Constants.num_rounds+1))
                probabilities = Constants.probability
                lottery_hi = Constants.lottery_hi
                lottery_lo = Constants.lottery_lo
                endowments = Constants.endowment

                p.participant.vars['ce_environment'] = list(zip(round_list, endowments, lottery_hi, lottery_lo,
                                                                probabilities))
                p.participant.vars['ce'] = [None for j in range(0, Constants.num_rounds)]
                p.participant.vars['ce_outcomes'] = [None for j in range(0, Constants.num_rounds)]


class Group(BaseGroup):
    rnd_draw = models.FloatField()
    rnd_bdm = models.FloatField()
    payoff = models.FloatField()
    winner = models.IntegerField()
    ce = models.CurrencyField()
    selection = models.IntegerField()

    def set_group_payoffs(self, round_num):
        # self.random_round = randrange(1, Constants.num_rounds + 1)
        # if the randomly drawn number is smaller than the specified probability, then win the lottery
        self.rnd_draw = random()
        # determine the BDM draw. lower bound and upper bound are the
        self.rnd_bdm = rrandom.uniform(Constants.lottery_lo[round_num - 1], Constants.lottery_hi[round_num - 1])

        if self.rnd_draw < self.get_player_by_id(1).participant.vars['ce_environment'][round_num - 1][4]:
            self.winner = 1
        else:
            self.winner = 0

        endowment = Constants.endowment[round_num - 1]

        dd = random()
        for k in range(0, Constants.players_per_group):
            if Constants.cum_weight[k] < dd < Constants.cum_weight[k + 1]:
                self.ce = self.get_player_by_id(k + 1).participant.vars['ce'][self.round_number - 1]
                self.selection = k + 1

        if self.rnd_bdm > self.ce:
            self.payoff = self.rnd_bdm
        else:
            if self.winner == 1:
                self.payoff = Constants.lottery_hi[round_num - 1]
            else:
                self.payoff = Constants.lottery_lo[round_num - 1]

        for p in self.get_players():
            p.payoff = self.payoff*(1/3)
            p.participant.vars['ce_outcomes'][round_num - 1] = [self.ce, self.rnd_draw, self.rnd_bdm, p.payoff,
                                                                self.winner, p.payoff + endowment]


class Player(BasePlayer):

    ce = models.CurrencyField(
        doc="""The amount you choose for your group""",
    )

    def set_participant_investment(self, round_num):
        self.participant.vars['ce'][round_num - 1] = self.ce
