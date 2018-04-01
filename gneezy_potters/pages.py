from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _
import random
from random import random
from random import randrange

def vars_for_all_templates(self):
    round_number = self.subsession.round_number
    return{
        'endowment': c(self.player.participant.vars['environment'][round_number - 1][1]),
        'probability': round(self.player.participant.vars['environment'][round_number - 1][2], 2),
        'return': round(self.player.participant.vars['environment'][round_number - 1][3] - 1, 2)
    }


class Instruction(Page):
    # Only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1


class Investment(Page):
    form_model = 'player'
    form_fields = ['investment']

    timeout_submission = {'investment': c(0)}

    # def vars_for_template(self):
    #     round_number = self.subsession.round_number
    #     return{
    #         'endowment': c(self.player.participant.vars['environment'][round_number - 1][1]),
    #         'probability': self.player.participant.vars['environment'][round_number - 1][2],
    #         'return': self.player.participant.vars['environment'][round_number - 1][3] - 1
    #     }

    def before_next_page(self):
        round_number = self.subsession.round_number
        self.player.set_payoffs(round_number)


# class ResultsWaitPage(WaitPage):
#
#     def after_all_players_arrive(self):
#         pass


class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    def vars_for_template(self):

        # round_num = self.subsession.round_number
        rand_num = randrange(1, Constants.num_rounds + 1)
        # unzip <cem_choices> into list of lists
        choices = self.participant.vars['environment'][rand_num - 1]
        endowment = choices[1]
        probability = round(choices[2], 2)
        return_rate = round(choices[3] - 1, 2)


        self.participant.payoff = self.participant.vars['payoff'][rand_num - 1]

        return {
            'round_to_pay': rand_num,
            'chosen_endowment': endowment,
            'chosen_investment': self.participant.vars['investment'][rand_num - 1],
            'chosen_probability': probability,
            'chosen_return': return_rate,
            'payoff': self.participant.vars['payoff'][rand_num - 1],
        }



page_sequence = [
    Instruction,
    Investment,
    Results
]
