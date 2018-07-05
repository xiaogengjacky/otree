
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random as rrandom
import itertools
from random import *
from statistics import median


class Constants(BaseConstants):
    name_in_url = 'wta_wtp_gap'
    players_per_group = None
    num_rounds = 1
    indicator = True

    floor_val = c(0)
    ceiling_val = c(40)


class Subsession(BaseSubsession):

    def creating_session(self):
        treatments = itertools.cycle(['wtp', 'wta'])
        for p in self.get_players():
            p.treatment = next(treatments)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bid = models.CurrencyField(
        min=Constants.floor_val, max=Constants.ceiling_val,
        doc="""你的心理价位""",
    )

    rnd_bdm = models.FloatField()
    pay = models.FloatField()
    winner = models.IntegerField()
    treatment = models.StringField()

    def set_participant_investment(self):
        # self.random_round = randrange(1, Constants.num_rounds + 1)
        # if the randomly drawn number is smaller than the specified probability, then win the lottery
        # determine the BDM draw. lower bound and upper bound are the
        self.rnd_bdm = rrandom.uniform(Constants.floor_val, Constants.ceiling_val)

        # wtp players
        if self.treatment == 'wtp':
            if self.rnd_bdm > self.bid:
                self.pay = 0
                self.winner = 0
            else:
                self.pay = self.rnd_bdm
                self.winner = 1

        elif self.treatment == 'wta':
            if self.rnd_bdm > self.bid:
                self.pay = self.rnd_bdm
                self.winner = 0
            else:
                self.pay = 0
                self.winner = 1


