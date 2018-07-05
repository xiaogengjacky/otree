from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):

        if self.player.treatment == 'wtp':
            return {'bid_template': 'wta_wtp_gap/BidWtp.html'}
        elif self.player.treatment == 'wta':
            return {'bid_template': 'wta_wtp_gap/BidWta.html'}


class Result(Page):

    def vars_for_template(self):

        self.player.set_participant_investment()

        if self.player.treatment == 'wtp':
            if self.player.winner == 1:
                outcome = '成功'
            else:
                outcome = '没有'

            return {'result_template': 'wta_wtp_gap/ResultWtp.html',
                    'outcome': outcome,
                    'payoff': c(self.player.pay),
                    'price': c(self.player.rnd_bdm),
                    'bid': self.player.bid}

        elif self.player.treatment == 'wta':
            if self.player.winner == 0:
                outcome = '成功'
            else:
                outcome = '没有'
            return {'result_template': 'wta_wtp_gap/ResultWta.html',
                    'outcome': outcome,
                    'payoff': c(self.player.pay),
                    'price': c(self.player.rnd_bdm),
                    'bid': self.player.bid
                    }


class BidWtp(Page):

    pass


class BidWta(Page):

    pass


class ResultWta(Page):

    pass


class ResultWtp(Page):

    pass


page_sequence = [
    Bid,
    Result
]



