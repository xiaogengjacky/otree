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
        'group_size': Constants.players_per_group,
        'endowment': c(Constants.endowment[round_number - 1]),
        'high': c(Constants.lottery_hi[round_number - 1]),
        'low': c(Constants.lottery_lo[round_number - 1]),
        'probability': format(Constants.probability[round_number - 1], ",.0%"),
        'probability_r': format(1 - Constants.probability[round_number - 1], ",.0%")
    }
# --------------------------------------------------------------------------------------------------------------------


class Instruction(Page):
    # Only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1
# --------------------------------------------------------------------------------------------------------------------


class Decision(Page):
    form_model = 'player'
    form_fields = ['ce']

    timeout_submission = {'ce': c(0)}

    def ce_max(self):
        if Constants.lottery_hi[self.subsession.round_number - 1] > 0:
            return Constants.lottery_hi[self.subsession.round_number - 1]
        else:
            return Constants.lottery_lo[self.subsession.round_number - 1]

    def ce_min(self):
        if Constants.lottery_hi[self.subsession.round_number - 1] > 0:
            return Constants.lottery_lo[self.subsession.round_number - 1]
        else:
            return Constants.lottery_hi[self.subsession.round_number - 1]

    def before_next_page(self):
        round_num = self.subsession.round_number
        self.player.set_participant_investment(round_num)
# --------------------------------------------------------------------------------------------------------------------


class Pausepage(Page):

    def is_displayed(self):
        # for passing values to the next app
        self.participant.vars['ce_rand_round'] = self.subsession.chosen_rnd_round

        return self.subsession.round_number == Constants.num_rounds

# --------------------------------------------------------------------------------------------------------------------


class Results(Page):
    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    def vars_for_template(self):

        rand_round = self.subsession.chosen_rnd_round
        ce_p = self.player.participant.vars['ce_outcomes'][rand_round - 1][0]

        choices = self.participant.vars['ce_environment'][rand_round - 1]
        endowment = choices[1]
        high = choices[2]
        low = choices[3]
        probability = choices[4]

        if self.player.in_round(rand_round).winner == 1:
            outcome = c(high)
        else:
            outcome = c(low)

        if self.player.in_round(rand_round).rnd_bdm > self.player.in_round(rand_round).ce:
            receive = "the sure amount"
        else:
            receive = "the lottery payout"



        return {
            'round_to_pay': rand_round,
            'ce_p': ce_p,
            'high': c(high),
            'low': c(low),
            'chosen_endowment': c(endowment),
            'chosen_probability': format(probability, ",.0%"),
            'rnd_bdm': format(self.player.in_round(rand_round).rnd_bdm, ",.2f"),
            'outcome': outcome,
            'receive': receive,
            'payoff': self.player.in_round(rand_round).payoff,
            'final_payoff': self.player.in_round(rand_round).payoff + Constants.endowment[rand_round]
        }


page_sequence = [
    Instruction,
    Decision,
    # ResultsWaitPage,
]

if not Constants.results:
    page_sequence.append(Pausepage)

if Constants.results:
    page_sequence.append(Results)