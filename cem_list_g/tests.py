from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


# **********************************************************************************************************************
# *** BOT
# **********************************************************************************************************************
class PlayerBot(Bot):

    def play_round(self):

        # define page as round_number
        page = self.subsession.round_number

        # get bot's switching point
        switching_point = self.player.participant.vars['cem_list_g-bot_switching_point']

        # ------------------------------------------------------------------------------------------------------------ #
        # submit instructions page
        # ------------------------------------------------------------------------------------------------------------ #
        if Constants.instructions:
            if page == 1:
                yield (pages.Instructions)

        # ------------------------------------------------------------------------------------------------------------ #
        # make decisions
        # ------------------------------------------------------------------------------------------------------------ #
        indices = [list(t) for t in zip(*self.player.participant.vars['cem_choices'][page - 1])][0]
        form_fields = [list(t) for t in zip(*self.player.participant.vars['cem_choices'][page - 1])][1]

        decisions = []
        for i in indices:
            if i <= switching_point:
                decisions.append('A')
            else:
                decisions.append('B')

        choices = zip(form_fields, decisions)
        yield (pages.Decision, {
            i: j for i, j in choices
        })

        # ------------------------------------------------------------------------------------------------------------ #
        # submit results page
        # ------------------------------------------------------------------------------------------------------------ #
        if Constants.results:
            if page == Constants.num_rounds:
                yield (pages.Results)