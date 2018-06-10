from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    def is_displayed(self):
        return self.player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def vars_for_template(self):
        if self.player.id_in_group == 2:
            # body_text = "You are participant 2. Waiting for participant 1 to decide."
            body_text = "你是角色2。请等候角色1做出决定。"
        else:
            # body_text = 'Please wait'
            body_text = "请等候"
        return {'body_text': body_text}


class Results(Page):
    def offer(self):
        return Constants.endowment - self.group.kept

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
        }


page_sequence = [
    Introduction,
    Offer,
    ResultsWaitPage,
    Results
]
