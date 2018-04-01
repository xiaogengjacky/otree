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
        'probability': self.player.participant.vars['environment'][round_number - 1][2],
        'return': self.player.participant.vars['environment'][round_number - 1][3] - 1
    }
# --------------------------------------------------------------------------------------------------------------------


class Instruction(Page):
    # Only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1
# --------------------------------------------------------------------------------------------------------------------


class Investment(Page):
    form_model = 'player'
    form_fields = ['investment']

    timeout_submission = {'investment': c(0)}

    def before_next_page(self):
        round_num = self.subsession.round_number
        self.player.set_participant_investment(round_num)

    # def vars_for_template(self):
    #     round_number = self.subsession.round_number
    #     return{
    #         'endowment': c(self.player.participant.vars['environment'][round_number - 1][1]),
    #         'probability': self.player.participant.vars['environment'][round_number - 1][2],
    #         'return': self.player.participant.vars['environment'][round_number - 1][3] - 1
    #     }

# --------------------------------------------------------------------------------------------------------------------


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_group_payoffs()

# --------------------------------------------------------------------------------------------------------------------


class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    def vars_for_template(self):

        rand_num = self.player.group.random_round
        id_self = self.player.id_in_group
        id_other1 = self.player.get_others_in_group()[0].id_in_group
        id_other2 = self.player.get_others_in_group()[1].id_in_group
        investment_p = self.player.participant.vars['investment'][rand_num - 1]
        investment_p1 = self.player.get_others_in_group()[0].participant.vars['investment'][rand_num - 1]
        investment_p2 = self.player.get_others_in_group()[1].participant.vars['investment'][rand_num - 1]
        # unzip <cem_choices> into list of lists
        choices = self.participant.vars['environment'][rand_num - 1]
        round_num = choices[0]
        endowment = choices[1]

        self.participant.payoff = self.participant.vars['payoff']

        return {
            'round_to_pay': rand_num,
            'id_self': id_self,
            'id_other1': id_other1,
            'id_other2': id_other2,
            'investment_p': investment_p,
            'investment_p1': investment_p1,
            'investment_p2': investment_p2,
            'endowment': c(endowment),
            'payoff': self.participant.vars['payoff']
        }


page_sequence = [Investment,
                 ResultsWaitPage]

if Constants.instruction:
    page_sequence.insert(0, Instruction)

if Constants.results:
    page_sequence.append(Results)
