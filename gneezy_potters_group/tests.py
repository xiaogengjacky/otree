from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # num_rounds = Constants.num_rounds
        if self.subsession.round_number == 1:
            yield (pages.Instruction)
        yield (pages.Investment, {'investment': self.player.id_in_group*10 + 30})
        if self.subsession.round_number == Constants.num_rounds:
            if Constants.combined:
                yield (pages.Ceresults)
                yield (pages.Results)
            else:
                yield (pages.Results)

