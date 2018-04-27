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
#     ----------------------------------------------------------------------------------------------------------------
class Ceresults(Page):

    def is_displayed(self):

        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        rand_round = self.participant.vars['ce_rand_round']
        choices = self.participant.vars['ce_environment'][rand_round - 1]

        endowment = choices[1]
        high = choices[2]
        low = choices[3]
        probability = choices[4]

        if self.participant.vars['ce_outcomes'][rand_round - 1][4] == 1:
            outcome = c(high)
        else:
            outcome = c(low)

        if self.participant.vars['ce_outcomes'][rand_round - 1][2] > self.participant.vars['ce_outcomes'][rand_round - 1][0]:
            receive = "the sure amount"
        else:
            receive = "the lottery payout"

        return {
            'high': c(high),
            'low': c(low),
            'chosen_probability': format(probability, ",.0%"),
            'round_to_pay': rand_round,
            'ce_p': self.participant.vars['ce_outcomes'][rand_round - 1][0],
            'payoff': self.participant.vars['ce_outcomes'][rand_round - 1][3],
            'rnd_bdm': self.participant.vars['ce_outcomes'][rand_round - 1][2],
            'outcome': outcome,
            'receive': receive,
            'final_payoff': self.participant.vars['ce_outcomes'][rand_round - 1][3] + endowment
        }


class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    def vars_for_template(self):

        # round_num = self.subsession.round_number
        rand_num = self.subsession.rand_round
        # unzip <cem_choices> into list of lists
        choices = self.participant.vars['environment'][rand_num - 1]
        endowment = choices[1]
        probability = round(choices[2], 2)
        return_rate = round(choices[3] - 1, 2)

        if self.player.winner == 1:
            outcome = "successful"
        else:
            outcome = "unsuccessful"

        if Constants.combined:
            rand_round = self.participant.vars['ce_rand_round']
            self.participant.payoff = self.participant.vars['payoff'][rand_num - 1] \
                                      + self.participant.vars['ce_outcomes'][rand_round - 1][5]
        else:
            self.participant.payoff = self.participant.vars['payoff'][rand_num - 1]

        return {
            'round_to_pay': rand_num,
            'chosen_endowment': endowment,
            'chosen_investment': self.participant.vars['investment'][rand_num - 1],
            'chosen_probability': probability,
            'chosen_return': return_rate,
            'outcome': outcome,
            'payoff': self.participant.vars['payoff'][rand_num - 1],
        }

# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #

page_sequence = [
    Instruction,
    Investment,
    Results
]

if Constants.combined:
    page_sequence.insert(2, Ceresults)
