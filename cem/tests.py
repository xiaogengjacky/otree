from otree.api import Currency as c, currency_range
from . import views
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
        switching_point = self.player.participant.vars['cem-bot_switching_point']

        # ------------------------------------------------------------------------------------------------------------ #
        # submit instructions page
        # ------------------------------------------------------------------------------------------------------------ #
        if Constants.instructions:
            if Constants.one_choice_per_page:
                if page == 1:
                    yield (views.Instructions)
            else:
                yield (views.Instructions)

        # ------------------------------------------------------------------------------------------------------------ #
        # make decisions
        # ------------------------------------------------------------------------------------------------------------ #
        indices = [list(t) for t in zip(*self.player.participant.vars['cem_choices'])][0]
        form_fields = [list(t) for t in zip(*self.player.participant.vars['cem_choices'])][1]

        if Constants.one_choice_per_page:
            if indices[page - 1] <= switching_point:
                yield (views.Decision, {
                    form_fields[page - 1]: 'A'
                })
            else:
                yield (views.Decision, {
                    form_fields[page - 1]: 'B'
            })

        else:
            decisions = []
            for i in indices:
                if i <= switching_point:
                    decisions.append('A')
                else:
                    decisions.append('B')

            choices = zip(form_fields, decisions)
            yield (views.Decision, {
                i: j for i, j in choices
            })

        # ------------------------------------------------------------------------------------------------------------ #
        # submit results page
        # ------------------------------------------------------------------------------------------------------------ #
        if Constants.results:
            if Constants.one_choice_per_page:
                if page == Constants.num_choices:
                    yield (views.Results)
            else:
                yield (views.Results)