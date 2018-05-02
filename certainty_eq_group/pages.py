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
        'group_endowment': c(Constants.endowment[round_number - 1]*Constants.players_per_group),
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


class ResultsWaitPage(WaitPage):

    def is_displayed(self):
        # return self.round_number == Constants.num_rounds
        return True

    def after_all_players_arrive(self):
        self.group.set_group_payoffs(self.subsession.round_number)
# --------------------------------------------------------------------------------------------------------------------


class Pausepage(Page):

    def is_displayed(self):
        # values for the next app
        rand_round = self.subsession.chosen_rnd_round
        id_self = self.player.id_in_group
        id_other1 = self.player.get_others_in_group()[0].id_in_group
        id_other2 = self.player.get_others_in_group()[1].id_in_group
        ce_p = self.player.participant.vars['ce'][rand_round - 1]
        ce_p1 = self.player.get_others_in_group()[0].participant.vars['ce'][rand_round - 1]
        ce_p2 = self.player.get_others_in_group()[1].participant.vars['ce'][rand_round - 1]

        self.participant.vars['rand_round'] = rand_round
        self.participant.vars['result_info'] = [id_self, id_other1, id_other2, ce_p, ce_p1, ce_p2,
                                                self.group.in_round(rand_round).payoff]
        return self.subsession.round_number == Constants.num_rounds
# --------------------------------------------------------------------------------------------------------------------


class Results(Page):
    # skip results until last page
    def is_displayed(self):
        # if Constants.one_choice_per_page:
        return self.subsession.round_number == Constants.num_rounds
        # return True

    def vars_for_template(self):

        rand_round = self.subsession.chosen_rnd_round
        id_self = self.player.id_in_group
        id_other1 = self.player.get_others_in_group()[0].id_in_group
        id_other2 = self.player.get_others_in_group()[1].id_in_group
        ce_p = self.player.participant.vars['ce'][rand_round - 1]
        ce_p1 = self.player.get_others_in_group()[0].participant.vars['ce'][rand_round - 1]
        ce_p2 = self.player.get_others_in_group()[1].participant.vars['ce'][rand_round - 1]

        choices = self.participant.vars['ce_environment'][rand_round - 1]
        endowment = choices[1]
        high = choices[2]
        low = choices[3]
        probability = choices[4]

        if self.player.group.in_round(rand_round).winner == 1:
            outcome = c(high)
        else:
            outcome = c(low)

        if self.player.group.in_round(rand_round).rnd_bdm > self.player.group.in_round(rand_round).ce:
            receive = "the sure amount"
        else:
            receive = "the lottery payout"

        return{
            'round_to_pay': rand_round,
            'id_self': id_self,
            'id_other1': id_other1,
            'id_other2': id_other2,
            'ce_p': ce_p,
            'ce_p1': ce_p1,
            'ce_p2': ce_p2,
            'high': c(high),
            'low': c(low),
            'group_ce': self.player.group.in_round(rand_round).ce,
            'chosen_endowment': c(endowment),
            'chosen_probability': format(probability, ",.0%"),
            'rnd_bdm': format(self.group.in_round(rand_round).rnd_bdm, ",.2f"),
            'group_payoff': c(round(self.group.in_round(rand_round).payoff, 0)),
            'outcome': outcome,
            'receive': receive,
            'payoff': self.player.in_round(rand_round).payoff,
            'final_payoff': self.player.in_round(rand_round).payoff + Constants.endowment[rand_round]
        }


page_sequence = [
    Instruction,
    Decision,
    ResultsWaitPage,
]

if not Constants.results:
    page_sequence.append(Pausepage)

if Constants.results:
    page_sequence.append(Results)